# Aesthetic Design

**Public edition 1.0.0:** 36 textual guides and 43 provenance records, with only **9 bundled images across 8 directions**; **28 directions lack local visual comparators**. Read [publication policy](materials/publication-policy.json). Use only assets marked `availability: included`; withheld paths are provenance identifiers, not existing files. Do not automatically download withheld images. For a missing comparator, state the visual gap, lower visual-attribution confidence and use a lawfully supplied input if available. Text alone cannot support a claim of inspected imagery.

An Agent Skill for identifying, comparing, auditing, and applying aesthetic/design styles. It includes 36 reference guides and catalogued images of real works spanning branding, graphic design, interfaces, products, and spaces.

[中文](README.zh-CN.md) · [Skill instructions](SKILL.md) · [Reference handbook](references/README.md)

## Package

```text
aesthetic-design/
  SKILL.md
  SKILL.zh-CN.md
  README.md
  README.zh-CN.md
  references/
    README.md
    01-rational-modern/
    02-eastern-traditions/
    03-western-classics/
    04-materials-and-everyday-life/
    05-decoration-and-experimentation/
    06-digital-and-futures/
  materials/
    README.md
    catalog.json
    styles/
  scripts/
    validate_offline.py
```

Instructions, the handbook, and all 36 guides have corresponding translations using the .zh-CN suffix. Both document sets link to the same materials catalog and files; materials are not duplicated by language. Responses follow the user's language. This public repository is self-contained; the complete private research-image collection is not distributed.

## Install and discover

Copy the **whole aesthetic-design folder**, including references, into one of these locations:

| Host | Project scope | Personal scope |
|---|---|---|
| Codex | `.agents/skills/aesthetic-design/` | `~/.agents/skills/aesthetic-design/` |
| Claude Code | `.claude/skills/aesthetic-design/` | `~/.claude/skills/aesthetic-design/` |

Codex's documented skill locations and symlink support are described in [OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills). Claude Code documents its directories, symlinks, and invocation in [Anthropic's skill documentation](https://code.claude.com/docs/en/skills).

Optionally keep one canonical installed folder under `.agents/skills/` and link `.claude/skills/aesthetic-design` to it. These discovery directories and links are an installation choice, not entries already present in this repository. Install the folder in the project where you need it; a nested folder is not automatically a project-root installation.

To reproduce this shared-folder setup on a system with symbolic-link support, run the following from the project containing the canonical `.agents/skills/aesthetic-design` folder, provided the Claude entry does not already exist:

```sh
mkdir -p .claude/skills
ln -s ../../.agents/skills/aesthetic-design .claude/skills/aesthetic-design
```

If symlinks are unavailable, copy the full package into each host's supported location and update both copies together. Do not copy only SKILL.md. Avoid extra same-name copies in multiple Codex discovery locations.

For Claude account-based skills, import the standalone package using that product's skill-management interface; local Claude Code directories do not by themselves install it in every Claude web or cloud environment. Consult the [Claude availability rules](https://code.claude.com/docs/en/skills#use-skills-in-cowork-and-cloud-sessions).

## Use

| Host | Explicit invocation example |
|---|---|
| Codex | `$aesthetic-design Compare this poster with Swiss Style and Bauhaus.` |
| Claude Code | `/aesthetic-design Compare this poster with Swiss Style and Bauhaus.` |

You can also request a matching task in natural language. If a local installation does not appear, first check its directory, complete references, and host discovery state; a fresh session is a simple fallback. Host configuration, trust, or organization policy can affect availability.

Example requests:

- Identify the plausible styles in this unlabeled interior image and explain what remains uncertain.
- Compare Song-inspired objects, Literati Ink, Ming Style, and Neo-Chinese for this brand brief.
- Design a Neo-Chinese + Minimalist exhibition page; show how both rule sets organize the result.
- Audit this claimed Bauhaus poster against its core criteria and the nearest alternative.

## Offline execution

The source collection has 43 scoped reference records; this public edition bundles 9 images and withholds 34; the two weak context-only views have been removed. Read the [correspondence review](materials/correspondence-review.md) for the revised selections and easily confused groups. The catalog separates `reference_asset_ids` from `context_asset_ids`; background images cannot stand alone as positive style evidence. Full per-image selection decisions are in the [selection review](materials/selection-review.md).

Start at the [materials entry point](materials/README.md) and [catalog](materials/catalog.json). Each style has a same-numbered note under `materials/styles/`, linking named real works, their source records, visible evidence, and limits. The catalog identifies actual local images and their records; inspect availability rather than assume every external candidate has been downloaded.

Read the candidate's guide and material note, inspect its actual local image when possible, and cite the asset ID and record. Identify whether the comparator is an artwork, photograph, object, building, historical proposal, or published interface. Material notes summarize evidence; they are not complete source-page caches. A catalogued comparator does not establish a newly supplied object's identity, process, or intention.

Downloaded images and local records remain available without network access. When an image is missing or only an external preview is listed, disclose that visual-comparison gap. The optional package checker is:

    python3 scripts/validate_offline.py

Use each asset record's source, rights, attribution, and scope. Public previews are not automatically freely reusable; unknown or restricted rights remain explicit. An integrity check can detect file problems, but does not authenticate historical objects, measure model accuracy, or prove coverage of every style branch. External URLs remain provenance and optional enrichment for already available local evidence.

## Behavior and limits

- Historical identity, visible formal language, and actual influence/process receive separate conclusions.
- Core organizing relationships matter more than palette, material names, or isolated motifs.
- Multiple styles may divide roles or jointly constrain the same structure.
- Unknown styles start with observed evidence and candidates; the 36-guide collection is not exhaustive.
- Finished designs return to the attribution workflow. Unsupported claims require revision or an honest reduction in scope; relabeling does not fulfill an unmet target-style requirement.
- Quality, usability, accessibility, and authenticity are separate questions. Unseen artifacts and untested interactions remain unverified.

The package uses the shared name/description frontmatter and ordinary relative Markdown references. It has no host-specific tool names, inline shell execution, hooks, required scripts, API keys, or mandatory external services. Online evidence may still be needed for a new historical or causal claim.

Compatibility checks establish package structure and reference consistency. They do not establish successful activation in every Codex/Claude version or image-classification accuracy. Source access dates retained in the translated guides are the original research dates, not fresh verification dates.

## Version and maintenance

Current version: **1.0.0**. Read [CHANGELOG.md](CHANGELOG.md), the [per-release record](changes/1.0.0.md), [MAINTENANCE.md](MAINTENANCE.md), and [third-party notices](THIRD_PARTY_NOTICES.md). Original instructions/analysis/code use [MIT](LICENSE); third-party content retains its own terms. This is the conservative public edition; the complete private image archive is excluded.
