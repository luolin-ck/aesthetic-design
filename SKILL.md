---
name: aesthetic-design
description: >-
  Identify, compare, audit, or apply aesthetic and design styles across brand
  identity, graphic design, web/UI, products, interiors, and architecture. Use
  for style attribution, distinctions between related styles, style-led design
  briefs, and checking whether a finished design supports its claimed style.
  Includes 36 reference guides with catalogued real-work visual materials;
  the collection is not an exhaustive taxonomy.
metadata:
  version: 1.0.0
---

**Public edition 1.0.0:** 36 textual guides and 43 provenance records, with only **9 bundled images across 8 directions**; **28 directions lack local visual comparators**. Read [publication policy](materials/publication-policy.json). Use only assets marked `availability: included`; withheld paths are provenance identifiers, not existing files. Do not automatically download withheld images. For a missing comparator, state the visual gap, lower visual-attribution confidence and use a lawfully supplied input if available. Text alone cannot support a claim of inspected imagery.


# Aesthetic Design

Use observable organizing relationships to identify or apply a style. Keep historical identity, visible formal language, and actual creative influence separate. Do not classify by counting colors, materials, or cultural symbols.

## Runtime and language

- This is a portable Agent Skill for Codex and Claude Code with local guides, real-work images, and linked object/source records. Use the host's available file-reading, image-viewing, and authoring tools; no particular tool name, script, dependency, or model is required.
- Resolve every reference path relative to the directory containing this SKILL.md, regardless of the current working directory or the host's discovery path.
- Read references progressively. Start with the relevant guides, then expand when comparison or branch coverage requires it. Do not load the entire collection by default.
- Respond in the user's requested language; otherwise follow the language of the conversation. Corresponding translated instructions and guides use the .zh-CN suffix, including [SKILL.zh-CN.md](SKILL.zh-CN.md). Both document sets use the same materials catalog and files; materials are not duplicated by language.
- Match claims to available evidence. If an image, rendered page, source, or interaction cannot be inspected, state what remains unverified. Never claim that a planned visual or interaction was observed.
- For installation and host-specific invocation, see [README.md](README.md).

## Offline evidence contract

- **Use the real-work materials as the local comparison path.** Read the candidate's guide, then locate its entry in [materials/catalog.json](materials/catalog.json) and its same-numbered note under [materials/styles](materials/README.md). Each guide links its exact material note. Read only the entries needed for the task.
- In `catalog.styles`, use `style_id`, `guide`, `material_note`, and `asset_ids` to find the relevant `catalog.assets` entries, their actual local images, and linked records. Inspect those images with the host's visual tools. A remote candidate or preview URL is not an inspected local image; check the recorded availability before claiming offline coverage.
- Read each record's `reference_role`, `claim_scope`, `association_evidence`, and `confusion_check` before using it. `reference_asset_ids` are scoped branch comparators; `context_asset_ids` are historical/site/method background. A `context_only` image must not establish membership by itself. Different views of one project are complementary views, not independent positive examples. Compare the nearest alternative using the stated organizing relationships, and allow broader/narrower or overlapping attributions.
- Use each source only for the specific object, version and fact it documents. Keep direct image observations and editorial style comparisons separate from source-stated facts. A catalog record for another example of the same model does not establish the photographed object's maker, manufacture date or hidden construction.
- Name the real work, creator/date when documented, medium or regional branch, and the specific organizing relationships visible in the inspected image. Cite its asset ID and local record. Text notes summarize evidence and limits; they are not cached full source pages. Retrieval or packaging dates do not establish the creation date of a work or photograph.
- Compare actual artworks, objects, buildings, or published interfaces. Do not substitute an authored schematic, generated image, invented webpage, or generic mood image for a real comparator. A concept drawing may itself be a real published work, but identify its medium and do not present it as a photograph of a built object. Several crops or derivatives of one image are not independent corroboration.
- A documented work is not automatically a useful comparator. Choose a view where the branch-defining relationships are visible at a readable size, with adequate exposure and minimal obstruction or unrelated salient content. Tourists, vehicles, display stacks, filming equipment, portraits and sensational headlines can dominate perception. Replace or exclude a weak view rather than using attribution or a long caveat to compensate; preserve genuine published images and disclose any remaining limits. Do not discard complexity that is itself the evidence, such as coordinated maximalist layers or a cyberpunk infrastructure/sign network. Minor ordinary context may remain only when it neither hides nor dominates the defining relationships.
- Respect each record's rights and attribution. A publicly visible preview is not necessarily openly licensed, and a photograph license does not automatically clear the depicted work. Keep unknown rights and restrictions explicit; do not describe unresolved candidates as freely reusable assets.
- If a new object's date, maker, actual material, hidden join, authorization, influence, or psychological claim is not established by the supplied input or local record, leave that claim unverified. A formally supported attribution may still proceed. Do not invent unavailable details to compensate for isolation.
- When only text can be read, use the guide and material note while stating which visual details could not be inspected. If the relevant image is absent, unavailable, or fails integrity checking, report the affected visual-comparison gap. Do not silently substitute memory, an imagined image, or an inaccessible URL as inspected evidence.
- New information, outside-collection styles, or a request for current primary-source verification may require additional supplied records or network access. In an isolated environment, state that specific limit and continue the supported part. Lack of network access alone does not invalidate this collection's local formal criteria.
- The downloaded files listed in the catalog can be inspected without a network connection; external source URLs remain provenance and optional enrichment. This does not promise offline visual evidence for an entry with no local image. An optional integrity check is available at [scripts/validate_offline.py](scripts/validate_offline.py); analysis does not require executing it. File integrity is not historical authentication, visual-classification accuracy, or proof that every branch is represented.

## Workflow A: Identify, compare, or audit a style

Use this workflow for labeled or unlabeled images, screenshots, objects, descriptions, or code, including questions such as "What style is this?" and "Does this count as Bauhaus?"

1. **Define the object and the claim.**
   - Specify whether the object is a chair, an entire room, a poster layout, one page, or a whole website. A room corner cannot establish the whole interior's style; a product photograph cannot establish the website's layout language.
   - Distinguish three claims:
     - **Historical, regional, or original-work identity:** requires records of dates, authorship, workshop/manufacturer, commissioning, or relevant scholarship. Separate the original design date from the manufacture or reproduction date of the object being examined.
     - **Contemporary formal language:** compare observable organizing rules with the relevant criteria and historical examples. The creator's reference list is not a prerequisite for a visual comparison.
     - **Actual influence, method, or intention:** requires process records, documented statements, or other evidence of the specific causal claim. Appearance alone does not establish a creator's references, technique, beliefs, or psychology.

2. **Build candidates from visible evidence before retrieving guides.**
   - Record the lines, planes, proportions, connections, pattern relationships, information hierarchy, or spatial sequences that can actually be observed. Mark what cannot be seen. User labels, filenames, and marketing copy are claims to check.
   - If the user names a style, treat it as a candidate and include plausible neighbors that explain the same evidence. Cover all styles the user explicitly asks to compare.
   - For an unlabeled input, propose initial candidates from the observed relationships and medium, explain why each is plausible, and read their criteria. Reading 1–3 guides is a useful first pass, not a hard limit; color or a material name alone cannot lock the candidate set.
   - The 36 guides are not exhaustive. Expand beyond the first candidates or beyond this collection when needed. Check outside directions against verifiable material rather than forcing the nearest listed label. If such material is unavailable, describe the visible relationships and mark the proposed direction as unverified. Absence from the index is not counterevidence.

3. **Test organizing relationships, not a surface checklist.**
   - Read each candidate's **Attribution Criteria**, including **Scope and Claims**, **Core Evidence Dimensions**, and the applicable medium, branch, and alternative explanations. Use its catalogued real-work image, local record, and material note for concrete comparison. When the required image is present locally, an external page need not open; otherwise disclose the visual-evidence gap.
   - Identify which structural, proportional, component, pattern, or image/text relationships jointly organize the main object. Red/yellow/blue does not establish Bauhaus; beige and empty space do not establish Song-inspired design or Wabi-sabi; purple neon does not establish Cyberpunk.
   - Decoration may itself organize contours, boundaries, or the viewing sequence. Do not impose functionalism or removal of ornament as a universal membership rule.

4. **Compare neighbors and test a counterfactual.**
   - Read **Combined Judgment and Neighboring Styles** and use the comparison table below as a prompt, not a replacement for branch-specific criteria.
   - Could the nearest alternative explain the same evidence? Would replacing a surface symbol leave the organizing relationships unchanged? Which conclusion would change if a core grid, connection, or spatial relationship changed?
   - Expand the reading if another candidate or branch remains plausible. If the input lacks the discriminating detail, stop forcing a narrower label: report insufficient evidence and specify the most useful missing view or record.
   - Styles can overlap or stand in broader/narrower relationships. A broader attribution or an explicit explanation of that relationship is preferable to an unsupported exclusive label.

5. **Evaluate membership separately from quality.**
   - A cramped, low-contrast poster may still use a recognizable style. An expensive, comfortable, well-made, or handmade object may not belong to the claimed style.
   - Usability, accessibility, material safety, fabrication quality, and aesthetic success require separate evaluation. Neither poor quality nor a low price automatically cancels visible stylistic membership.

6. **Report a conclusion for each relevant claim.**
   - Answer the claims the user asks about or those needed to clarify the attribution. Do not force every analysis into one label or invent unrelated authenticity questions.
   - **Historical/regional identity:** report "historical/regional attribution established," "insufficient evidence for historical/regional attribution," or "direct counterevidence to the identity claim," citing the specific records or conflict. Answer original-design identity and present-object manufacture/reproduction identity separately.
   - **Visible formal language:** use the five terms below for the specified object or layer only.
   - **Actual influence, method, or intention:** state whether the particular claim is supported by process records/documented statements, lacks evidence, or faces direct counterevidence. Formal resemblance does not prove causation.
   - Use these formal-attribution terms:
     - **Primary style:** identifiable organizing rules jointly govern the main object. State the relationships, locations, and why a more specific attribution is justified over a neighbor.
     - **Local borrowing:** a particular region, graphic, or component corresponds to the language without organizing the whole. Name what is borrowed and what governs the whole. Mere color resemblance should be called color resemblance.
     - **Mixed:** two or more identifiable rule sets have meaningful roles. Explain their respective locations and how they divide responsibilities or jointly constrain the same structure. One need not be reduced to decoration.
     - **Attribution not supported:** visible main relationships conflict with the claimed formal language, or there is direct counterevidence to that formal claim. Limit the conclusion to what was examined; assess historical dates separately.
     - **Insufficient evidence:** the available view cannot distinguish plausible formal explanations. Identify the missing full view, component detail, plan, or content. A missing date alone does not prevent a sufficiently supported visual judgment.
   - Missing information is not counterevidence. These terms are working vocabulary, not official certification or a numerical qualification system.
   - Check that the formal conclusion can complete this statement: "For [object/scope] at the [visual layer], the conclusion is [term], because [relationships and evidence]. Its relationship to [neighbor] is [correspondence, distinction, or unresolved ambiguity]. The relevant missing evidence is [if any]."
   - Example: records may establish a teapot's Bauhaus original design while contemporary production records establish that the examined object is newly made. Its visible component relationships can still follow that design. None of these facts independently proves early manufacture, authorization, or use of the original workshop method.

## Workflow B: Design with a style or reinterpret it for a new medium

Use this workflow for style-led posters, identities, pages/UI, products, or spaces.

1. **Define the practical brief.**
   - Identify the medium, audience, and core task, such as helping a first-time visitor find exhibition tickets within five seconds. Read the relevant style guides.

2. **Translate criteria into inspectable design decisions.**
   - Read **Attribution Criteria** and the corresponding real-work material note and images before **Design Philosophy**, **Design Language**, and **Practical Design Methods**. Disclose any unavailable image or unrepresented branch.
   - Map "criterion → design action → intended location in the artifact." This is the basis for later verification, not a requirement to hit a fixed number of features.
   - Specify how composition, axes, grid modules, spacing, and hierarchy organize the content; how color/material treatment participates in that organization; and how graphics, type, and ornament generate contours, divisions, or narrative.
   - Use the selected branch's actual rules. Avoid substituting a generic palette, typeface, geometric motif, or vague mood for the style's discriminating relationships.

3. **Reinterpret for the actual medium.**
   - Historical paintings, architecture, and furniture do not prescribe modern buttons. Select valid translations such as layout structure, spacing rhythm, connected contours, image narrative, or border/shadow relationships without forcing every style into the same component treatment.
   - Keep navigation, buttons, forms, focus states, and text legible and usable under the relevant modern interaction and accessibility requirements.

4. **Explain how multiple styles combine.**
   - Identify each style's recognizable rules, where they act, and how they combine. One can lead with local borrowing from another; styles can govern different regions/layers; or both can constrain the same layout, component, or spatial relationship.
   - For Neo-Chinese + Minimalism, traditional framing and title-panel divisions might organize information while reduction and density rhythm refine the same layout. Japanese spatial relationships and Nordic furniture can jointly organize heights, sightlines, and component relationships.
   - Resolve conflicts through specific adjustments and explain the choice. If one contribution is only similar coloring, say so; two names alone do not establish a meaningful fusion.

5. **Test real content and common misreadings.**
   - Use realistic short/long content, data, and interaction states, then check **Related Styles and Common Misreadings**.
   - If actual content is unavailable, identify sample material and untested states instead of claiming real-content verification.

6. **Return the actual artifact to Workflow A for style acceptance.**
   - Inspect the deliverable rather than repeating its design intent. Briefly record "core criterion → actual location and observable evidence → neighboring explanation and distinction → conclusion and changes needed."
   - For mixed styles, check each contribution's independent evidence and their combination. When a guide requires comparison with a historical example, inspect the named real-work image and its local object/source record, then identify the structural correspondence; generic functionality or geometry is insufficient. A comparator's record cannot replace evidence about the new object's provenance.
   - If core relationships do not appear, revise and check again. If only local borrowing, a broader direction, or insufficient evidence is supported, lower the claim honestly. Do not invent structures or influence to preserve a label. If the user requires the target style and it remains unmet, report that requirement as unfinished; relabeling alone does not fulfill it.
   - Match acceptance to the artifact: a written concept supports concept-level checking, not a claim that a rendered visual was verified. A cropped screenshot does not establish an entire website. Inspect available finished artifacts and explicitly mark unseen or untested parts.
   - Report style acceptance separately from usability, accessibility, and production quality. Record and fix quality defects without using them to erase a supported style attribution. Give the user a concise account of the actual relationships, scope, and remaining limitations.

## Reference index

Use the host's available file-reading tools. Start with 1–3 relevant guides when appropriate; expand for a larger explicit comparison, unresolved neighbors, or a specific branch. See the [reference handbook](references/README.md) for methodology and worked examples.

**Index entries are candidate-retrieval clues, not necessary-feature lists or sufficient evidence.** Missing a common feature cannot by itself exclude a branch. Check the medium, identity claim, and complete criteria before concluding. Appearance does not establish materials, hidden construction, dates, nationality, or beliefs.

### 01 Rational Modern

| Style | Concept type | Observation and design entry point | Guide |
|---|---|---|---|
| Bauhaus | Historical school and its influence | Specific workshop/historical examples and component/layout correspondence; functionality alone is insufficient | [01-bauhaus.md](references/01-rational-modern/01-bauhaus.md) |
| De Stijl | Art and design movement | Independent planes/lines and asymmetric balancing; includes orthogonal studies and Van Doesburg's diagonal branch | [02-de-stijl.md](references/01-rational-modern/02-de-stijl.md) |
| Swiss Style | Graphic and typographic tradition | Column grids, typographic information coding, image/text axes, and hierarchy | [03-swiss-style.md](references/01-rational-modern/03-swiss-style.md) |
| Modernism | Cross-disciplinary movements and ideas | Modern life, functional/structural relationships, reduction of redundant ornament, industrial production | [04-modernism.md](references/01-rational-modern/04-modernism.md) |
| Minimalism | Art movement and broader design orientation | Reduced element types, repeated modules, material presence, and spatial perception | [05-minimalism.md](references/01-rational-modern/05-minimalism.md) |
| Mid-Century Modern | Cross-regional mid-20th-century design label | Organic contact surfaces, light supports, molded plywood, and material experiments | [06-mid-century-modern.md](references/01-rational-modern/06-mid-century-modern.md) |

### 02 Eastern Traditions and Reinterpretation

| Style | Concept type | Observation and design entry point | Guide |
|---|---|---|---|
| Song Dynasty Objects | Period-specific object reference | Vessel proportions, glaze/light relationships, and coordinated use contexts | [07-song-dynasty-objects.md](references/02-eastern-traditions/07-song-dynasty-objects.md) |
| Literati Ink | Chinese painting and cultural tradition | Ink relationships, meaningful unpainted space, and interactions among poem, calligraphy, painting, and seals | [08-literati-ink.md](references/02-eastern-traditions/08-literati-ink.md) |
| Ming Style | Furniture-centered style concept | Frame/void proportions, curves, and molding transitions; timber, hidden joints, and dates require separate evidence | [09-ming-style.md](references/02-eastern-traditions/09-ming-style.md) |
| Imperial Court Decoration | Cross-period court production category | Ceremonial hierarchy, axial sequences, framed-field/border levels, and combined craft languages | [10-imperial-court-decoration.md](references/02-eastern-traditions/10-imperial-court-decoration.md) |
| Neo-Chinese | Contemporary design/market label | Traditional components, framing, or title-panel relationships reorganized for contemporary content and use | [11-neo-chinese.md](references/02-eastern-traditions/11-neo-chinese.md) |
| Wabi-sabi | Japanese aesthetic concept | Restrained viewing organization foregrounding individual irregularity and time-related traces | [12-wabi-sabi.md](references/02-eastern-traditions/12-wabi-sabi.md) |

### 03 Western Historical Classics

| Style | Concept type | Observation and design entry point | Guide |
|---|---|---|---|
| Classical | Greco-Roman tradition and later influence | Orders and their component chains, bay modules, and vertical hierarchy | [13-classical.md](references/03-western-classics/13-classical.md) |
| Gothic | Medieval architectural/artistic tradition | Pointed arches, ribbed structural relationships, vertical articulation, and tracery/light | [14-gothic.md](references/03-western-classics/14-gothic.md) |
| Renaissance | Historical cultural/artistic period | Reorganized classical components, coherent geometric modules, and perspective space | [15-renaissance.md](references/03-western-classics/15-renaissance.md) |
| Baroque | Historical artistic/architectural language | Converging movement, layered depth, frame crossing, and dramatic light relationships | [16-baroque.md](references/03-western-classics/16-baroque.md) |
| Rococo | Historical decorative/artistic language | C/S curves and rocaille, local non-mirrored responses, and contour-generating ornament | [17-rococo.md](references/03-western-classics/17-rococo.md) |
| Neoclassical | Historical artistic/design reform | Archaeological classical references, clear panel divisions, and controlled ornamental hierarchy | [18-neoclassical.md](references/03-western-classics/18-neoclassical.md) |

### 04 Materials and Everyday Life

| Style | Concept type | Observation and design entry point | Guide |
|---|---|---|---|
| Arts and Crafts | Historical design reform movement | Labor/craft context, flat interwoven repeat patterns, and medium-specific boundaries | [19-arts-and-crafts.md](references/04-materials-and-everyday-life/19-arts-and-crafts.md) |
| Nordic | Regional design traditions | Modern domestic branch: identifiable contours/components and spatial coordination; other directions retain an archival route | [20-nordic.md](references/04-materials-and-everyday-life/20-nordic.md) |
| Japandi | Contemporary interior/furnishing fusion label | Japanese spatial references and Nordic furniture jointly adjusted within the same setting | [21-japandi.md](references/04-materials-and-everyday-life/21-japandi.md) |
| Industrial | Interior/furnishing label | Visible structural/service relationships and factory-building references; actual age/materials need separate evidence | [22-industrial.md](references/04-materials-and-everyday-life/22-industrial.md) |
| Mediterranean | Regional architecture/interior label | Responses to coastal light/ventilation, thick walls/arches, plaster, and local material relationships | [23-mediterranean.md](references/04-materials-and-everyday-life/23-mediterranean.md) |
| Bohemian / Boho | Lifestyle and furnishing label | Heterogeneous furnishings, layered textiles, and cross-source color/texture relationships | [24-bohemian.md](references/04-materials-and-everyday-life/24-bohemian.md) |

### 05 Decoration and Experimentation

| Style | Concept type | Observation and design entry point | Guide |
|---|---|---|---|
| Art Nouveau | Historical art/design movement | Lines/ornament generate contours and divisions; includes Vienna/Glasgow geometric branches, not only curves | [25-art-nouveau.md](references/05-decoration-and-experimentation/25-art-nouveau.md) |
| Art Deco | Historical decorative/architectural language | Axes, stepping, radiation, repeated geometry, streamlining, and worked surfaces | [26-art-deco.md](references/05-decoration-and-experimentation/26-art-deco.md) |
| Memphis | Historical group and its influence | Unconventional geometric/component assembly, contrasting surfaces, and challenges to conventional typologies; overall symmetry is possible | [27-memphis.md](references/05-decoration-and-experimentation/27-memphis.md) |
| Pop Art | Modern art movement/visual culture | Recontextualized mass-media imagery, printing languages, recoloring, and repeated series | [28-pop-art.md](references/05-decoration-and-experimentation/28-pop-art.md) |
| Surrealism | Literary/visual art movement | Figurative entry: sustained displacement of familiar relationships; abstract/automatist claims need their own process/documentary route | [29-surrealism.md](references/05-decoration-and-experimentation/29-surrealism.md) |
| Maximalism | Cross-media design orientation | Dense layered patterns, colors, and heterogeneous objects organized by recurring motifs | [30-maximalism.md](references/05-decoration-and-experimentation/30-maximalism.md) |

### 06 Digital and Futures

| Style | Concept type | Observation and design entry point | Guide |
|---|---|---|---|
| Cyberpunk | Speculative genre and visual culture | High-tech systems versus individual circumstances, infrastructure/everyday friction, and layered artificial light | [31-cyberpunk.md](references/06-digital-and-futures/31-cyberpunk.md) |
| Retrofuturism | Reinterpretation of past futures | An identifiable past period's imagined technology/life viewed through a later temporal frame | [32-retrofuturism.md](references/06-digital-and-futures/32-retrofuturism.md) |
| Y2K | Turn-of-millennium culture and revival label | Virtual streamlined main forms, glossy/translucent shaping, and device-like modules; historical/revival identity is separate | [33-y2k.md](references/06-digital-and-futures/33-y2k.md) |
| Vaporwave | Internet music subculture and visual extension | Old commercial/system imagery organized through loops, distortion, and temporal collage; visual/music attribution is separate | [34-vaporwave.md](references/06-digital-and-futures/34-vaporwave.md) |
| Steampunk | Speculative genre and object culture | Victorian industrial/optical vocabulary and coherent imagined mechanical relationships | [35-steampunk.md](references/06-digital-and-futures/35-steampunk.md) |
| Web Brutalism | Digital design label | Distinguish raw document appearance, Neobrutalist hard-edged components, and Antidesign disruption | [36-web-brutalism.md](references/06-digital-and-futures/36-web-brutalism.md) |

## Quick comparisons

Use these questions to select and compare guides. They are not mutually exclusive certification rules.

| Neighbors | What to check first |
|---|---|
| [Bauhaus](references/01-rational-modern/01-bauhaus.md) / [De Stijl](references/01-rational-modern/02-de-stijl.md) | Bauhaus-like contemporary attribution needs specific historical component/layout correspondence; function alone is not enough. De Stijl-like language concerns independent planes/lines and asymmetric balancing, including orthogonal and diagonal branches. Check historical identity separately. |
| [Bauhaus](references/01-rational-modern/01-bauhaus.md) / [Swiss Style](references/01-rational-modern/03-swiss-style.md) | Swiss Style focuses on column systems, typographic information coding, and shared image/text axes. Primary colors on a modern grid do not by themselves establish Bauhaus. |
| [Art Nouveau](references/05-decoration-and-experimentation/25-art-nouveau.md) / [Art Deco](references/05-decoration-and-experimentation/26-art-deco.md) | Compare the generation of connected contours and ornamental divisions with axial, radiating, stepped, repeated, or streamlined decorative rhythm. Check the regional branch; curved versus straight is not a valid universal split. |
| [Baroque](references/03-western-classics/16-baroque.md) / [Rococo](references/03-western-classics/17-rococo.md) | Compare movement/depth/light converging into a dramatic event with local C/S rocaille relationships generating boundaries. Do not divide by public/private use or large/small scale; both can coexist in different layers. |
| [Minimalism](references/01-rational-modern/05-minimalism.md) / [Wabi-sabi](references/02-eastern-traditions/12-wabi-sabi.md) | Compare reduced modules and precise spacing with restrained viewing focused on individual variation and time-related traces. Neutral colors alone establish neither; use the relevant medium and branch. |
| [Y2K](references/06-digital-and-futures/33-y2k.md) / [Vaporwave](references/06-digital-and-futures/34-vaporwave.md) | Compare virtual streamlined/device-like shaping with loops, distortion, and temporal collage of old media. Do not infer classification or personal beliefs from optimistic/melancholic mood; both rule sets can jointly organize a work. |
| Architectural Brutalism / [Web Brutalism](references/06-digital-and-futures/36-web-brutalism.md) | Architectural history concerns physical structure and documented context. In web design, distinguish raw document appearance, hard-edged Neobrutalist components, and disrupted reading conventions. Appearance alone proves neither architectural identity nor a designer's intention. |

## Maintaining this skill

When changing this package, follow [MAINTENANCE.md](MAINTENANCE.md): write a failing acceptance check first, implement the smallest correction, record actual Red/Green evidence, increment VERSION, and update both changelogs and the per-version change record. This applies to package maintenance, not ordinary design tasks.
