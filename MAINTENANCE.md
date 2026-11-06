# Maintenance

[中文](MAINTENANCE.zh-CN.md)

VERSION is the single release-version source. Use stable SemVer: patch for corrections, minor for compatible new capability, major for incompatible changes. The first formal release is 1.0.0; earlier research was an unversioned baseline. Do not reconstruct old versions or tests from memory.

For every logical package change:

1. State the problem and observable acceptance in a new `changes/<version>.md` and its `.zh-CN.md` translation. Write a meaningful failing check before changing the behavior. For a factual/style correction, the check may be a documented, reproducible comparison against named primary evidence; do not force wording-only unit tests.
2. Run the check and save the actual failure, command, date and expected/actual result. Distinguish untested from failed. Never label an import error or missing dependency as a demonstrated stylistic defect.
3. Implement the smallest correction; rerun the acceptance and relevant existing checks. Record actual Green results, limitations, affected paths and rollback. An automated check verifies integrity and metadata, not visual accuracy or copyright clearance.
4. Increase VERSION; synchronize both SKILL metadata blocks, `materials/manifest.json`, both CHANGELOG files, and `changes/<version>.json`. Keep older records. Each record lists every logical change in that release; do not silently fold a later change into an issued version.
5. Update original and Chinese documents together outside materials. Machine data, executable test logic and the canonical MIT text are shared; do not mechanically duplicate them. No translated copies belong inside materials.
6. Update catalog/records/notes together. Recompute each manifest file's byte count and SHA-256 after all content changes, excluding the manifest itself and `.git`. Preserve all existing integrity and availability checks. Public media needs an exact path/hash allowlist, image rights and depicted-work rights; never promote an excluded image just to improve coverage.
7. Run the commands below with Python 3.9 or later. Before a later release, also run `python3 -B scripts/check_release.py --base-version <previous-published-version>` so unchanged/decreasing versions fail. Review the actual diff for unlogged changes; metadata tests cannot prove that every editorial decision was logged.

```sh
python3 -B -m unittest discover -s tests -v
python3 -B scripts/validate_offline.py
python3 -B scripts/validate_offline.zh-CN.py
python3 -B scripts/check_release.py
```

The scripts are read-only and standard-library-only. They do not download, install, execute supplied material, or contact services. Run them from a clean package; Python caches and unrelated files are deliberately rejected. The integrity manifest is not a build recipe: regeneration must not be used to approve unknown files. For distribution, independently review the complete file tree, media decisions, license scope and Git author/commit history before publishing. Keep a full private collection outside the public Git history; no full-image archive may be attached to a public release.

A change record contains version/previous version, problem, scope, logical changes, acceptance, real Red/Green evidence, remaining limits and rollback. The JSON companion supports automated consistency checks; the prose records what was actually tested. To roll back, restore the last verified complete distribution or Git tag, then rerun validation; do not erase the intervening log. Offline host compatibility checks do not prove activation in every Codex or Claude Code version.
