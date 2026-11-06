#!/usr/bin/env python3
"""使用标准库只读校验真实作品素材包。

不联网获取、不调用模型、不渲染、不安装、不写文件。
只检查完整性与记录字段，不证明风格分类准确率、真实性或使用权。
"""

import ast
from datetime import date
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import socket
import struct
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

sys.dont_write_bytecode = True
from check_release import validate_release

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "materials/manifest.json"
LIMITS = "只检查完整性与记录字段，不证明风格分类准确率、真实性或使用权。"
MESSAGES = {
    "network": "本校验进程已禁用网络",
    "path": "路径无效或超出技能包：{value}",
    "read": "无法读取 {path}：{error}",
    "json": "JSON对象无效：{path}：{error}",
    "list": "应为对象列表：{label}",
    "item": "对象无效：{label}[{index}]",
    "duplicate": "标识或路径重复、无效：{label}",
    "file_set": "清单文件集不一致；缺失={missing}；多出={extra}",
    "entry": "清单字节数或哈希字段无效：{path}",
    "size": "字节数不一致：{path}",
    "hash": "SHA-256不一致：{path}",
    "utf8": "UTF-8文本无效：{path}",
    "link": "本地链接失效或越界：{path} -> {target}",
    "anchor": "Markdown或HTML锚点不存在：{path} -> {target}",
    "uri": "不支持的URI：{path} -> {target}",
    "remote_image": "存在远程图片依赖：{path} -> {target}",
    "old_materials": "已废弃或按语言重复的素材路径：{path}",
    "old_link": "仍引用已废弃素材：{path}",
    "style_count": "应恰好包含36种编号风格",
    "style_field": "风格字段{field}无效：{style_id}",
    "mapping": "指南与素材映射不一致：{style_id}",
    "reference_partition": "风格参照与语境素材的分区无效或角色不一致：{style_id}",
    "sections": "指南必须包含规定的九节：{path}",
    "guide_set": "编号指南文件缺失或多出",
    "pairs": "应恰好有40对译本：39对Markdown及1对Python",
    "pair_target": "译本对应关系异常：{original} -> {translation}",
    "pair_set": "译本文件集不一致",
    "python": "Python语法无效：{path}：{error}",
    "logic": "两个校验脚本译本的执行逻辑不同",
    "asset_count": "清单asset_count与目录素材数量不同",
    "asset_field": "素材字段{field}无效：{asset_id}",
    "asset_set": "存在未映射素材或风格映射缺少素材",
    "record_set": "目录未恰好覆盖materials/records内的JSON记录",
    "image_set": "目录未恰好覆盖本地JPEG与PNG图片",
    "record_field": "记录字段{field}缺失或无效：{asset_id}",
    "record_match": "目录与记录字段{field}不一致：{asset_id}",
    "review": "图片缺少有日期、范围的视觉复核记录：{asset_id}",
    "image": "JPEG或PNG数据、扩展名无效：{path}：{error}",
    "dimensions": "图片尺寸与记录不同：{path}",
    "summary": "校验完成，共{count}项错误。"
}

SLUGS = [
    "bauhaus", "de-stijl", "swiss-style", "modernism", "minimalism", "mid-century-modern",
    "song-dynasty-objects", "literati-ink", "ming-style", "imperial-court-decoration",
    "neo-chinese", "wabi-sabi", "classical", "gothic", "renaissance", "baroque",
    "rococo", "neoclassical", "arts-and-crafts", "nordic", "japandi", "industrial",
    "mediterranean", "bohemian", "art-nouveau", "art-deco", "memphis", "pop-art",
    "surrealism", "maximalism", "cyberpunk", "retrofuturism", "y2k", "vaporwave",
    "steampunk", "web-brutalism",
]
GROUPS = [
    "01-rational-modern", "02-eastern-traditions", "03-western-classics",
    "04-materials-and-everyday-life", "05-decoration-and-experimentation",
    "06-digital-and-futures",
]
STYLE_GUIDES = {
    f"{number:02d}-{slug}": f"references/{GROUPS[(number - 1) // 6]}/{number:02d}-{slug}.md"
    for number, slug in enumerate(SLUGS, 1)
}
SECTIONS = [
    "Attribution Criteria", "Position and Background", "Design Philosophy",
    "Design Language", "Practical Design Methods", "Design Example",
    "Representative Cases and Application Boundaries",
    "Related Styles and Common Misreadings", "Sources",
]
SECTIONS_ZH = [
    "归属判定标准", "定位与背景", "设计理念", "设计语言", "实践设计方法",
    "设计示例", "代表案例与应用边界", "相近风格与常见误读", "来源",
]
RIGHTS = {"open_license", "public_domain", "restricted_public_preview"}
REFERENCE_ROLES = {"style_reference", "context_only"}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
OBSOLETE = re.compile(
    r"style-packets|(?:^|/)visuals(?:/|$)|source-register|(?:^|/)evaluation(?:/|$)"
    r"|materials/sources/"
)
ERRORS = []
BYTE_CACHE = {}
TEXT_CACHE = {}


def message(key, **values):
    return MESSAGES[key].format(**values)


def check(condition, key, **values):
    if not condition:
        ERRORS.append(message(key, **values))
    return bool(condition)


def deny_network(*args, **kwargs):
    raise OSError(message("network"))


# 禁止本进程创建网络套接字或查询DNS，也约束将来误加的联网调用。
socket.socket = deny_network
socket.create_connection = deny_network
socket.getaddrinfo = deny_network
socket.gethostbyname = deny_network
socket.gethostbyname_ex = deny_network


def translated_path(relative):
    path = Path(relative)
    return path.with_name(path.stem + ".zh-CN" + path.suffix).as_posix()


def local_path(relative):
    if not isinstance(relative, str) or not relative or "\\" in relative:
        check(False, "path", value=repr(relative))
        return None
    candidate = Path(relative)
    if candidate.is_absolute() or candidate.as_posix() != relative or ".." in candidate.parts:
        check(False, "path", value=relative)
        return None
    resolved = (ROOT / candidate).resolve()
    if not resolved.is_relative_to(ROOT):
        check(False, "path", value=relative)
        return None
    return resolved


def read_bytes(relative):
    if relative not in BYTE_CACHE:
        path = local_path(relative)
        try:
            BYTE_CACHE[relative] = path.read_bytes() if path else b""
        except OSError as error:
            check(False, "read", path=relative, error=error)
            BYTE_CACHE[relative] = b""
    return BYTE_CACHE[relative]


def read_text(relative):
    if relative not in TEXT_CACHE:
        try:
            TEXT_CACHE[relative] = read_bytes(relative).decode("utf-8")
        except UnicodeDecodeError:
            check(False, "utf8", path=relative)
            TEXT_CACHE[relative] = ""
    return TEXT_CACHE[relative]


def load_json(relative):
    try:
        value = json.loads(read_text(relative))
        if not isinstance(value, dict):
            raise ValueError("object")
        return value
    except ValueError as error:
        check(False, "json", path=relative, error=error)
        return {}


def objects(value, label):
    if not check(isinstance(value, list), "list", label=label):
        return []
    result = []
    for index, item in enumerate(value):
        if check(isinstance(item, dict), "item", label=label, index=index):
            result.append(item)
    return result


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def valid_review_date(value, latest):
    try:
        return date.fromisoformat(value).isoformat() == value and date.fromisoformat(value) <= date.fromisoformat(latest)
    except (TypeError, ValueError):
        return False


def integer(value):
    return type(value) is int and value > 0


def http_url(value):
    if not isinstance(value, str):
        return False
    try:
        parts = urlsplit(value)
        return parts.scheme in {"http", "https"} and bool(parts.netloc)
    except ValueError:
        return False


def indexed(items, field, label):
    result = {}
    for item in items:
        value = item.get(field)
        if not check(nonempty(value) and value not in result, "duplicate", label=label):
            continue
        result[value] = item
    return result


def without_fences(text):
    lines = []
    fence = None
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(" + chr(96) + r"{3,}|~{3,})", line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            lines.append("")
        else:
            lines.append("" if fence else line)
    return "\n".join(lines)


class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for field in ("id", "name"):
            if attrs.get(field):
                self.anchors.add(attrs[field])
        if tag == "a" and attrs.get("href"):
            self.links.append((attrs["href"], False))
        if tag in {"img", "source"}:
            if attrs.get("src"):
                self.links.append((attrs["src"], True))
            if attrs.get("srcset"):
                for candidate in attrs["srcset"].split(","):
                    bits = candidate.strip().split()
                    if bits:
                        self.links.append((bits[0], True))


INLINE_LINK = re.compile(
    r"(!?)\[[^\]\n]*\]\(\s*(<[^>\n]*>|(?:\\.|[^()\s]|\([^()\n]*\))+)"
    r"(?:\s+(?:\"[^\"\n]*\"|'[^'\n]*'|\([^)\n]*\)))?\s*\)"
)
DEFINITION = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)", re.M)


def markdown_links(text):
    text = without_fences(text)
    parser = HTMLLinks()
    parser.feed(text)
    links = list(parser.links)
    for match in INLINE_LINK.finditer(text):
        links.append((match[2].strip("<>"), bool(match[1])))
    definitions = {m[1].strip().casefold(): m[2].strip("<>") for m in DEFINITION.finditer(text)}
    for match in re.finditer(r"(!?)\[([^\]\n]+)\](?:\[([^\]\n]*)\])?", text):
        key = (match[3] or match[2]).strip().casefold()
        if key in definitions:
            links.append((definitions[key], bool(match[1])))
    # Markdown中的CSS背景图片也属于远程图片依赖。
    for match in re.finditer(r"url\(\s*['\"]?([^)'\"\s]+)", text, re.I):
        links.append((match[1], True))
    return links, parser.anchors


def heading_anchors(text):
    plain = without_fences(text)
    headings = []
    lines = plain.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)(?:\s+#+)?\s*$", line)
        if match:
            headings.append(match[1])
        elif index and lines[index - 1].strip() and re.fullmatch(r"\s{0,3}(?:=+|-+)\s*", line):
            headings.append(lines[index - 1].strip())
    anchors = set()
    counts = {}
    for heading in headings:
        heading = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", heading)
        heading = html.unescape(re.sub(r"<[^>]+>", "", heading)).lower()
        slug = "".join(
            char for char in heading
            if char in "-_" or not unicodedata.category(char).startswith(("P", "S", "C"))
        )
        slug = re.sub(r"\s", "-", slug)
        number = counts.get(slug, 0)
        counts[slug] = number + 1
        anchors.add(slug + (f"-{number}" if number else ""))
    _, explicit = markdown_links(text)
    return anchors | explicit


def validate_links(relative):
    links, _ = markdown_links(read_text(relative))
    path = ROOT / relative
    for raw, image in links:
        target = html.unescape(raw)
        target = re.sub(r"\\([() <>])", r"\1", target)
        try:
            parts = urlsplit(target)
        except ValueError:
            check(False, "uri", path=relative, target=target)
            continue
        remote = parts.scheme in {"http", "https"} or bool(parts.netloc)
        if image and remote:
            check(False, "remote_image", path=relative, target=target)
            continue
        if remote:
            continue
        if parts.scheme:
            check(False, "uri", path=relative, target=target)
            continue
        file_part = unquote(parts.path)
        destination = (path.parent / file_part).resolve() if file_part else path.resolve()
        inside = destination.is_relative_to(ROOT)
        if not check(inside and destination.is_file(), "link", path=relative, target=target):
            continue
        if parts.fragment and destination.suffix.lower() == ".md":
            target_relative = destination.relative_to(ROOT).as_posix()
            check(unquote(parts.fragment) in heading_anchors(read_text(target_relative)),
                  "anchor", path=relative, target=target)
    return len(links)


def image_dimensions(data, suffix):
    # 直接读取PNG的IHDR或JPEG的SOF；不安装或调用图像库。
    if suffix == ".png":
        if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[8:16] != b"\x00\x00\x00\rIHDR":
            raise ValueError("PNG/IHDR")
        width, height = struct.unpack(">II", data[16:24])
        if b"IEND" not in data[-12:]:
            raise ValueError("PNG/IEND")
        if not width or not height:
            raise ValueError("PNG/dimensions")
        return width, height
    if suffix not in {".jpg", ".jpeg"} or data[:2] != b"\xff\xd8" or not data.endswith(b"\xff\xd9"):
        raise ValueError("JPEG/SOI/EOI")
    position = 2
    sof = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}
    while position < len(data):
        if data[position] != 0xFF:
            raise ValueError("JPEG/marker")
        while position < len(data) and data[position] == 0xFF:
            position += 1
        if position >= len(data):
            break
        marker = data[position]
        position += 1
        if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
            continue
        if marker == 0xDA or position + 2 > len(data):
            break
        length = int.from_bytes(data[position:position + 2], "big")
        if length < 2 or position + length > len(data):
            raise ValueError("JPEG/segment")
        if marker in sof:
            if length < 8:
                raise ValueError("JPEG/SOF")
            height, width = struct.unpack(">HH", data[position + 3:position + 7])
            if not width or not height:
                raise ValueError("JPEG/dimensions")
            return width, height
        position += length
    raise ValueError("JPEG/missing-SOF")


def python_logic(relative):
    try:
        tree = ast.parse(read_text(relative), filename=relative)
    except SyntaxError as error:
        check(False, "python", path=relative, error=error)
        return None
    # 仅忽略翻译后的消息、模块与函数文档字符串，以及注释。
    tree.body = [
        node for node in tree.body
        if not (isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id in {"MESSAGES", "LIMITS"} for t in node.targets))
    ]
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body = node.body[1:]
    return ast.dump(tree, include_attributes=False)


def main():
    manifest = load_json(MANIFEST)
    catalog = load_json("materials/catalog.json")
    actual_paths = {
        p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
        if p.is_file() and ".git" not in p.relative_to(ROOT).parts and p.relative_to(ROOT).as_posix() != MANIFEST
    }
    entries = objects(manifest.get("files"), "manifest.files")
    file_map = indexed(entries, "path", "manifest.files")
    expected = set(file_map)
    check(actual_paths == expected, "file_set",
          missing=sorted(expected - actual_paths), extra=sorted(actual_paths - expected))
    for relative, entry in file_map.items():
        good_fields = integer(entry.get("bytes")) and isinstance(entry.get("sha256"), str) and re.fullmatch(r"[a-f0-9]{64}", entry["sha256"])
        check(good_fields, "entry", path=relative)
        data = read_bytes(relative)
        check(len(data) == entry.get("bytes"), "size", path=relative)
        check(hashlib.sha256(data).hexdigest() == entry.get("sha256"), "hash", path=relative)
    for path in (ROOT / "materials").rglob("*"):
        relative = path.relative_to(ROOT).as_posix()
        check(".zh-CN" not in relative and not OBSOLETE.search(relative),
              "old_materials", path=relative)
        check(path.suffix.lower() not in {".svg", ".gif", ".webp"}, "old_materials", path=relative)
    md_paths = sorted(path for path in actual_paths if path.endswith(".md"))
    links_checked = 0
    for relative in md_paths:
        text = read_text(relative)
        check(not OBSOLETE.search(text), "old_link", path=relative)
        links_checked += validate_links(relative)

    originals = {path for path in actual_paths if path.endswith(".md") and ".zh-CN" not in path and not path.startswith("materials/")} | {"scripts/validate_offline.py"}
    expected_pairs = {path: translated_path(path) for path in originals}
    pairs = objects(manifest.get("translation_pairs"), "manifest.translation_pairs")
    pair_map = indexed(pairs, "original", "manifest.translation_pairs")
    check(len(pairs) == len(originals) and set(pair_map) == originals, "pairs")
    translations = set()
    for original, item in pair_map.items():
        translation = item.get("translation")
        check(translation == expected_pairs.get(original), "pair_target",
              original=original, translation=translation)
        if isinstance(translation, str):
            translations.add(translation)
            for relative in (original, translation):
                path = local_path(relative)
                check(path is not None and path.is_file(), "link", path=original, target=relative)
    actual_translations = {path for path in actual_paths if ".zh-CN" in path}
    check(translations == set(expected_pairs.values()) == actual_translations, "pair_set")
    check(python_logic("scripts/validate_offline.py") == python_logic("scripts/validate_offline.zh-CN.py"), "logic")

    styles = objects(catalog.get("styles"), "catalog.styles")
    style_map = indexed(styles, "style_id", "catalog.styles")
    check(len(styles) == 36 and set(style_map) == set(STYLE_GUIDES) and manifest.get("style_count") == 36, "style_count")
    assets = objects(catalog.get("assets"), "catalog.assets")
    asset_map = indexed(assets, "asset_id", "catalog.assets")
    check(type(manifest.get("asset_count")) is int and manifest["asset_count"] == len(assets) == len(asset_map), "asset_count")
    mapped_assets = []
    expected_notes = set()
    for style_id, style in style_map.items():
        expected_guide = STYLE_GUIDES.get(style_id)
        expected_note = f"materials/styles/{style_id}.md"
        expected_notes.add(expected_note)
        check(nonempty(style.get("style_name")), "style_field", field="style_name", style_id=style_id)
        check(style.get("guide") == expected_guide and style.get("material_note") == expected_note, "mapping", style_id=style_id)
        note_path = local_path(expected_note)
        check(note_path is not None and note_path.is_file(), "style_field", field="material_note", style_id=style_id)
        ids = style.get("asset_ids")
        valid_ids = isinstance(ids, list) and bool(ids) and all(nonempty(a) for a in ids)
        check(valid_ids, "style_field", field="asset_ids", style_id=style_id)
        if valid_ids:
            check(len(ids) == len(set(ids)), "style_field", field="asset_ids", style_id=style_id)
            for asset_id in ids:
                mapped_assets.append(asset_id)
                check(asset_id in asset_map and asset_map[asset_id].get("style_id") == style_id,
                      "style_field", field="asset_ids", style_id=style_id)
        reference_ids = style.get("reference_asset_ids")
        context_ids = style.get("context_asset_ids")
        valid_partition = (
            isinstance(reference_ids, list) and bool(reference_ids)
            and isinstance(context_ids, list)
            and all(nonempty(a) for a in reference_ids + context_ids)
        )
        check(valid_partition, "reference_partition", style_id=style_id)
        if valid_partition and valid_ids:
            check(len(reference_ids + context_ids) == len(set(reference_ids + context_ids))
                  and set(reference_ids + context_ids) == set(ids),
                  "reference_partition", style_id=style_id)
            for group_ids, role in [(reference_ids, "style_reference"), (context_ids, "context_only")]:
                check(all(a in asset_map and asset_map[a].get("reference_role") == role for a in group_ids),
                      "reference_partition", style_id=style_id)
        if expected_guide:
            for relative, headings in [(expected_guide, SECTIONS), (translated_path(expected_guide), SECTIONS_ZH)]:
                check(re.findall(r"^## (.+)$", without_fences(read_text(relative)), re.M) == headings,
                      "sections", path=relative)
    actual_notes = {p.relative_to(ROOT).as_posix() for p in (ROOT / "materials/styles").glob("*.md")}
    check(actual_notes == expected_notes, "mapping", style_id="materials/styles")
    expected_guides = set(STYLE_GUIDES.values())
    expected_guides |= {translated_path(path) for path in expected_guides}
    actual_guides = {path for path in md_paths if path.startswith("references/") and re.match(r"\d{2}-", Path(path).name)}
    check(actual_guides == expected_guides, "guide_set")
    check(set(mapped_assets) == set(asset_map) and len(mapped_assets) == len(set(mapped_assets)), "asset_set")

    image_paths = []
    record_paths = []
    text_fields = [
        "asset_id", "style_id", "object", "creator", "work_date", "rights",
        "rights_evidence", "attribution", "local_path", "rights_category", "reference_role", "claim_scope",
    ]
    for asset_id, asset in asset_map.items():
        style_id = asset.get("style_id")
        check(nonempty(style_id) and style_id in STYLE_GUIDES, "asset_field", field="style_id", asset_id=asset_id)
        for field in ("object", "local_path", "record_path", "rights_category", "reference_role"):
            check(nonempty(asset.get(field)), "asset_field", field=field, asset_id=asset_id)
        relative = asset.get("local_path")
        record_relative = asset.get("record_path")
        if not isinstance(relative, str) or not isinstance(record_relative, str):
            continue
        availability = asset.get("availability")
        check(availability in {"included", "withheld"} and (availability == "included" or manifest.get("distribution") == "public-conservative"),
              "asset_field", field="availability", asset_id=asset_id)
        if availability == "included":
            image_paths.append(relative)
        record_paths.append(record_relative)
        check(relative.startswith("materials/") and Path(relative).suffix.lower() in IMAGE_SUFFIXES,
              "asset_field", field="local_path", asset_id=asset_id)
        check(record_relative.startswith("materials/records/") and record_relative.endswith(".json"),
              "asset_field", field="record_path", asset_id=asset_id)
        record = load_json(record_relative)
        for field in text_fields:
            check(nonempty(record.get(field)), "record_field", field=field, asset_id=asset_id)
        for field in ("source_page", "downloaded_from"):
            check(http_url(record.get(field)), "record_field", field=field, asset_id=asset_id)
        for field in ("asset_id", "style_id", "object", "local_path", "rights_category", "reference_role", "availability"):
            check(record.get(field) == asset.get(field), "record_match", field=field, asset_id=asset_id)
        check(nonempty(record.get("rights_category")) and record["rights_category"] in RIGHTS, "record_field", field="rights_category", asset_id=asset_id)
        check(nonempty(record.get("reference_role")) and record["reference_role"] in REFERENCE_ROLES,
              "record_field", field="reference_role", asset_id=asset_id)
        association = objects(record.get("association_evidence"), asset_id + ".association_evidence")
        check(bool(association) and all(http_url(e.get("url")) and nonempty(e.get("supports")) for e in association),
              "record_field", field="association_evidence", asset_id=asset_id)
        confusion = record.get("confusion_check")
        check(isinstance(confusion, dict), "record_field", field="confusion_check", asset_id=asset_id)
        if isinstance(confusion, dict):
            alternatives = confusion.get("nearest_alternatives")
            check(isinstance(alternatives, list) and bool(alternatives) and all(nonempty(a) for a in alternatives),
                  "record_field", field="confusion_check.nearest_alternatives", asset_id=asset_id)
            for field in ("shared_appearances", "discriminating_relationships", "cannot_conclude"):
                value = confusion.get(field)
                check(nonempty(value) or isinstance(value, list) and bool(value) and all(nonempty(v) for v in value),
                      "record_field", field="confusion_check." + field, asset_id=asset_id)
        check("license_url" in record and (record["license_url"] is None or http_url(record["license_url"])),
              "record_field", field="license_url", asset_id=asset_id)
        for field in ("limits", "observable_features"):
            value = record.get(field)
            good = nonempty(value) if field == "limits" else isinstance(value, list) and bool(value) and all(nonempty(v) for v in value)
            if field == "limits" and isinstance(value, list):
                good = bool(value) and all(nonempty(v) for v in value)
            check(good, "record_field", field=field, asset_id=asset_id)
        review = record.get("visual_review")
        check(isinstance(review, dict) and review.get("status") == "reviewed"
              and valid_review_date(review.get("reviewed_on"), manifest.get("reviewed_on")) and nonempty(review.get("scope")),
              "review", asset_id=asset_id)
        for field in ("bytes", "width", "height"):
            check(integer(record.get(field)), "record_field", field=field, asset_id=asset_id)
        check(isinstance(record.get("sha256"), str) and bool(re.fullmatch(r"[a-f0-9]{64}", record["sha256"])),
              "record_field", field="sha256", asset_id=asset_id)
        if availability == "withheld":
            check(not (ROOT / relative).exists(), "asset_field", field="withheld image present", asset_id=asset_id)
            continue
        data = read_bytes(relative)
        check(len(data) == record.get("bytes"), "size", path=relative)
        check(hashlib.sha256(data).hexdigest() == record.get("sha256"), "hash", path=relative)
        try:
            width, height = image_dimensions(data, Path(relative).suffix.lower())
            check((width, height) == (record.get("width"), record.get("height")), "dimensions", path=relative)
        except (ValueError, struct.error) as error:
            check(False, "image", path=relative, error=error)
    actual_images = {path for path in actual_paths if Path(path).suffix.lower() in IMAGE_SUFFIXES}
    check(set(image_paths) == actual_images and len(image_paths) == len(set(image_paths)), "image_set")
    actual_records = {p.relative_to(ROOT).as_posix() for p in (ROOT / "materials/records").rglob("*.json")}
    check(set(record_paths) == actual_records and len(record_paths) == len(set(record_paths)), "record_set")
    check(all(path in file_map for path in image_paths + record_paths), "asset_set")

    ERRORS.extend(validate_release(ROOT))
    print(json.dumps({
        "result": "pass" if not ERRORS else "fail",
        "network": "disabled_in_validator_process",
        "files": len(entries), "styles": len(styles), "guides": len(actual_guides),
        "translation_pairs": len(pairs), "assets": len(assets),
        "images": len(image_paths), "local_links": links_checked,
        "errors": ERRORS, "message": message("summary", count=len(ERRORS)), "limits": LIMITS,
    }, ensure_ascii=False, indent=2))
    return 1 if ERRORS else 0


if __name__ == "__main__":
    sys.exit(main())
