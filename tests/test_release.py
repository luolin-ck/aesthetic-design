"""Small mutation tests for release boundaries; no network or external services."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_release.py"
spec = importlib.util.spec_from_file_location("check_release", SCRIPT)
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("materials/records", "materials/images", "changes"):
            (self.root / name).mkdir(parents=True)
        self.write("VERSION", "1.0.0\n")
        for name in ("SKILL.md", "SKILL.zh-CN.md"):
            self.write(name, "---\nname: aesthetic-design\nmetadata:\n  version: 1.0.0\n---\n")
        for name in ("CHANGELOG.md", "CHANGELOG.zh-CN.md"):
            self.write(name, "# Changes\n\n## [1.0.0]\n")
        for name in ("changes/1.0.0.md", "changes/1.0.0.zh-CN.md"):
            self.write(name, "# 1.0.0\n")
        self.record = {"version": "1.0.0", "previous_version": None,
                       "changes": ["Establish versioned releases"],
                       "acceptance": ["Reject unversioned releases"],
                       "red": {"actual_exit": 1, "expected_exit": 0},
                       "green": {"actual_exit": 0}}
        self.write_json("changes/1.0.0.json", self.record)
        self.write_json("materials/manifest.json", {"version": "1.0.0", "distribution": "private-complete"})
        self.write_json("materials/catalog.json", {"assets": []})

    def write(self, path, text):
        (self.root / path).write_text(text, encoding="utf-8")

    def write_json(self, path, value):
        self.write(path, json.dumps(value))

    def errors(self, **kwargs):
        return release.validate_release(self.root, **kwargs)

    def public_fixture(self):
        import hashlib
        self.write_json("materials/manifest.json", {"version": "1.0.0", "distribution": "public-conservative"})
        path = "materials/images/reference.jpg"
        (self.root / path).write_bytes(b"fixture historical image")
        sha = hashlib.sha256((self.root / path).read_bytes()).hexdigest()
        asset = {"asset_id": "reference", "local_path": path, "record_path": "materials/records/reference.json", "availability": "included"}
        self.write_json("materials/catalog.json", {"assets": [asset]})
        self.write_json(asset["record_path"], dict(asset, sha256=sha, rights_category="public_domain", rights="CC0", license_url="https://creativecommons.org/publicdomain/zero/1.0/"))
        self.write_json("materials/publication-policy.json", {"assets": [dict(asset, sha256=sha, decision="included", image_rights_basis="Institution designates this image CC0", depicted_work_basis="Historical public-domain work", evidence_urls=["https://example.org/object"])]})

    def test_valid_and_version_increase(self):
        self.assertEqual(self.errors(), [])
        self.assertTrue(self.errors(base_version="1.0.0"))
        self.assertEqual(self.errors(base_version="0.9.0"), [])

    def test_missing_version_and_log_rejected(self):
        (self.root / "VERSION").unlink()
        self.assertTrue(self.errors())
        self.write("VERSION", "1.0.0\n")
        (self.root / "changes/1.0.0.json").unlink()
        self.assertTrue(self.errors())

    def test_stale_frontmatter_and_red_evidence_requires_failure(self):
        self.write("SKILL.md", "---\nmetadata:\n  version: 0.9.0\n---\n\n  version: 1.0.0\n")
        self.assertTrue(self.errors())
        self.write("SKILL.md", "---\nmetadata:\n  version: 1.0.0\n---\n")
        self.record["red"]["actual_exit"] = 0
        self.write_json("changes/1.0.0.json", self.record)
        self.assertTrue(self.errors())

    def test_public_missing_and_unapproved_image_rejected(self):
        self.public_fixture()
        self.assertEqual(self.errors(), [])
        (self.root / "materials/images/extra.jpg").write_bytes(b"unapproved")
        self.assertTrue(self.errors())
        (self.root / "materials/images/extra.jpg").unlink()
        (self.root / "materials/images/reference.jpg").unlink()
        self.assertTrue(self.errors())

    def test_public_restricted_or_nc_cannot_be_allowlisted(self):
        self.public_fixture()
        path = "materials/records/reference.json"
        record = json.loads((self.root / path).read_text())
        record.update(rights_category="restricted_public_preview", rights="All rights reserved")
        self.write_json(path, record)
        self.assertTrue(self.errors())
        record.update(rights_category="open_license", rights="CC BY-NC-SA 4.0")
        self.write_json(path, record)
        self.assertTrue(self.errors())

    def test_secret_path_and_symlink_rejected(self):
        self.write("notes.md", "/" + "Users/example/private.txt")
        self.assertTrue(self.errors())
        self.write("notes.md", "gh" + "p_" + "X" * 36)
        self.assertTrue(self.errors())
        self.write("notes.md", "gh" + "o_" + "X" * 36)
        self.assertTrue(self.errors())
        (self.root / "notes.md").unlink()
        (self.root / "alias").symlink_to(self.root / "VERSION")
        self.assertTrue(self.errors())


if __name__ == "__main__":
    unittest.main()
