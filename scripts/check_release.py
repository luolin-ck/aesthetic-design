#!/usr/bin/env python3
"""Read-only release metadata and publication-boundary checks (standard library)."""
import argparse
import hashlib
import json
from pathlib import Path
import re

SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)")
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".txt"}


def validate_release(root, base_version=None):
    root = Path(root)
    errors = []
    links = [p.relative_to(root).as_posix() for p in root.rglob("*")
             if ".git" not in p.relative_to(root).parts and p.is_symlink()]
    if links:
        return ["Symlink forbidden in release: " + path for path in links]

    def require(condition, message):
        if not condition:
            errors.append(message)

    def text(relative):
        try:
            return (root / relative).read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append("Cannot read release text: " + relative)
            return ""

    def data(relative):
        try:
            value = json.loads(text(relative))
            if not isinstance(value, dict):
                raise ValueError()
            return value
        except (ValueError, TypeError):
            errors.append("Invalid release object: " + relative)
            return {}

    version = text("VERSION").strip()
    require(bool(SEMVER.fullmatch(version)), "VERSION must contain a stable SemVer")
    safe_version = version if SEMVER.fullmatch(version) else "invalid-version"
    manifest = data("materials/manifest.json")
    require(manifest.get("version") == version, "Manifest version differs from VERSION")
    edition = manifest.get("distribution")
    require(edition in {"private-complete", "public-conservative"}, "Unknown distribution profile")
    for path in ("SKILL.md", "SKILL.zh-CN.md"):
        content = text(path)
        frontmatter = content.split("\n---\n", 1)[0] if content.startswith("---\n") else ""
        metadata = re.search(r"^metadata:\s*\n((?:[ \t].*(?:\n|$))*)", frontmatter, re.M)
        versions = re.findall(r"^  version: (.+)$", metadata.group(1), re.M) if metadata else []
        require(versions == [version], "Skill metadata version differs: " + path)
    for path in ("CHANGELOG.md", "CHANGELOG.zh-CN.md"):
        require("## [" + version + "]" in text(path), "Current version absent from " + path)
    for suffix in (".md", ".zh-CN.md"):
        require(bool(text("changes/" + safe_version + suffix).strip()), "Missing human change record")
    record = data("changes/" + safe_version + ".json")
    require(record.get("version") == version, "Change-record version differs")
    for field in ("changes", "acceptance"):
        require(isinstance(record.get(field), list) and bool(record[field]), "Empty change-record " + field)
    red, green = record.get("red", {}), record.get("green", {})
    require(isinstance(red, dict) and red.get("actual_exit") != red.get("expected_exit")
            and type(red.get("actual_exit")) is int and type(red.get("expected_exit")) is int,
            "Red evidence must record an actual unmet expectation")
    require(isinstance(green, dict) and green.get("actual_exit") == 0, "Missing successful Green evidence")
    previous = record.get("previous_version")
    for earlier in (previous, base_version):
        if earlier is not None:
            require(isinstance(earlier, str) and bool(SEMVER.fullmatch(earlier)) and bool(SEMVER.fullmatch(version))
                    and tuple(map(int, version.split("."))) > tuple(map(int, earlier.split("."))),
                    "Release version must increase over previous/base version")
    catalog = data("materials/catalog.json")
    assets = catalog.get("assets", [])
    require(isinstance(assets, list), "Invalid asset list")
    assets = assets if isinstance(assets, list) else []
    if edition == "public-conservative":
        policy = data("materials/publication-policy.json")
        entries = policy.get("assets", [])
        require(isinstance(entries, list) and len(entries) == len(assets), "Publication decisions must cover every asset")
        entries = entries if isinstance(entries, list) else []
        decisions = {item.get("asset_id"): item for item in entries if isinstance(item, dict)}
        require(len(decisions) == len(entries) and set(decisions) == {a.get("asset_id") for a in assets},
                "Duplicate, missing or unknown publication decisions")
        approved = set()
        for asset in assets:
            decision = decisions.get(asset.get("asset_id"), {})
            status = decision.get("decision")
            path = asset.get("local_path", "")
            record_path = asset.get("record_path", "")
            safe = (isinstance(path, str) and path.startswith("materials/images/")
                    and ".." not in Path(path).parts and not Path(path).is_absolute())
            safe_record = (isinstance(record_path, str) and record_path.startswith("materials/records/")
                           and ".." not in Path(record_path).parts and not Path(record_path).is_absolute())
            require(safe and safe_record, "Unsafe asset path")
            if not safe or not safe_record:
                continue
            info = data(record_path)
            require(status in {"included", "withheld"} and asset.get("availability") == status
                    and info.get("availability") == status, "Asset availability is inconsistent: " + str(asset.get("asset_id")))
            require(decision.get("local_path") == path and decision.get("sha256") == info.get("sha256"),
                    "Publication decision path/hash mismatch: " + path)
            if status == "included":
                approved.add(path)
                rights = str(info.get("rights", "")) + " " + str(info.get("license_url", ""))
                require(info.get("rights_category") in {"public_domain", "open_license"}
                        and not re.search(r"\bNC\b|by-nc|non.?commercial|all rights reserved", rights, re.I),
                        "Restricted or noncommercial media cannot be included: " + path)
                require(all(decision.get(k) for k in ("image_rights_basis", "depicted_work_basis", "evidence_urls")),
                        "Missing separate image/work rights evidence: " + path)
                try:
                    require(hashlib.sha256((root / path).read_bytes()).hexdigest() == decision.get("sha256"),
                            "Approved media hash mismatch: " + path)
                except OSError:
                    errors.append("Missing approved media: " + path)
            else:
                require(bool(decision.get("reason")) and not (root / path).exists(), "Withheld media present or unexplained: " + path)
        actual = {p.relative_to(root).as_posix() for p in root.rglob("*")
                  if ".git" not in p.relative_to(root).parts and p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES}
        require(actual == approved, "Actual media differs from exact publication allowlist")
    forbidden_names = {".hermes", ".DS_Store", "__pycache__", ".env", ".netrc", "id_rsa", "id_ed25519"}
    secret = re.compile(r"gh" + r"[pousr]_[A-Za-z0-9]{30,}|github_" + r"pat_[A-Za-z0-9_]{30,}|sk-" + r"(?:proj-)?[A-Za-z0-9_-]{20,}|(?:AKIA|ASIA)[A-Z0-9]{16}|-----BEGIN " + r"(?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
    private_path = re.compile(r"/" + r"Users/[^/\s]+|/" + r"home/[^/\s]+|/private/" + r"var/|[A-Z]:\\" + r"Users\\", re.I)
    email = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I)
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if ".git" in relative.parts:
            continue
        require(not path.is_symlink(), "Symlink forbidden in release: " + relative.as_posix())
        require(not any(part in forbidden_names or part.startswith(".env.") for part in relative.parts),
                "Forbidden private/generated path: " + relative.as_posix())
        require(path.suffix.lower() not in {".zip", ".tar", ".gz", ".pem", ".key", ".p12", ".pfx"},
                "Archive or key forbidden in release: " + relative.as_posix())
        if path.is_file() and not path.is_symlink():
            if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"VERSION", "LICENSE", ".gitignore"}:
                try:
                    value = path.read_text(encoding="utf-8")
                    require(not secret.search(value), "Potential credential: " + relative.as_posix())
                    require(not private_path.search(value), "Private local path: " + relative.as_posix())
                    require(not email.search(value), "Email address requires removal/review: " + relative.as_posix())
                except (OSError, UnicodeError):
                    errors.append("Unreadable release text: " + relative.as_posix())
            elif edition == "public-conservative":
                require(path.suffix.lower() in IMAGE_SUFFIXES, "Unexpected binary/file type: " + relative.as_posix())
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-version", help="Require VERSION to be greater than the previous published version")
    args = parser.parse_args()
    errors = validate_release(Path(__file__).resolve().parents[1], args.base_version)
    print(json.dumps({"result": "fail" if errors else "pass", "errors": errors}, indent=2))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
