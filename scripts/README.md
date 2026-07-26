# Vocabulary Migration Scripts

One-off and reusable scripts for extracting word relationships from `notes`, applying nuance tags, and enriching the Anki CSV export. Most write to MongoDB via generated `mongosh` scripts.

**Run status checks with:**

```bash
mongosh "$MONGODB_URI" --file scripts/db_status_check.js
```

---

## Timeline of what was done

### Phase 1 — Relationship extraction (N3 → N2 → N1)

Parsed `rel:`, `sinonimo:`, `antonimo:` patterns from `notes` into structured `related[]` arrays (`wordId`, `type`, `note`). Links are bidirectional.

| Level | Scripts | Artifacts |
|-------|---------|-----------|
| N3 (earlier) | `analyze_relationships.py`, `migrate_relationships.py`, `n3_nuance_tags.py` | `relationship_analysis/`, `n3_relationships.json` |
| N2 (2026-05) | `n2_analyze_state.py` → `n2_extract_relationships.py` → `n2_generate_migration.py` | `n2_analysis/` |
| N1 (2026-05) | `n1_analyze_state.py` → `n1_extract_relationships.py` (+ apply scripts) | `n1_analysis/` |

Unresolved notes (target word missing, complex `～` patterns) stay in `notes` for later review — see `remaining_unresolved.json` / `unresolved.json` per level.

### Phase 2 — Nuance tagging by JLPT level

Tags describe how the **related** word differs from the source: `formal`, `casual`, `spoken`, `written`, `literary`, `technical`, `archaic`, `polite`, `humble`.

| Level | Tag definitions | Apply |
|-------|-----------------|-------|
| N3 | `n3_nuance_tags.py` | `apply_nuance_tags.py` / `.js` |
| N2 | `n2_nuance_tags.py` → `n2_apply_nuance_tags.py` | `n2_analysis/n2_apply_nuance_tags.js` |
| N1 | `n1_nuance_tags.py` → `n1_apply_nuance_tags.py` | `n1_analysis/n1_apply_nuance_tags.js` |

### Phase 3 — Untagged pair curation (2026-07)

Filled remaining synonym / antonym / related pairs that had no tags:

| Script | Purpose |
|--------|---------|
| `nuance_synonyms.py` | Curated synonym tags |
| `nuance_antonyms.py` | Curated antonym tags |
| `nuance_related_n3.py` / `n2` / `n1` | Related-type tags by level |
| `nuance_tags/*.js` | Generated mongosh apply scripts |
| `nuance_tags/curate_all_remaining.py` → `curate_all.js` | Final batch: ~440 unique pairs; applied bidirectionally with tag swaps (`formal`↔`casual`, `spoken`↔`written`) |
| `nuance_tags/propagate_reverse.js` | Fill reverse side when only one direction had tags |

**Result (2026-07-10):** 0 untagged related entries left in JLPT N1–N3. Removed one bad self-link (`推定` → itself).

### Phase 4 — Basic (text-only) related words

For everyday words the learner does **not** want as study cards (e.g. 天気 next to 天候):

| Script | Purpose |
|--------|---------|
| `basic_words_migration.py` | Defines pairs; generates mongosh |
| `basic_words/migrate.js` | `$addToSet` entries with `word` (string) instead of `wordId` |

UI/API: `POST/DELETE /words/<id>/related/basic` — no reverse link.

### Phase 5 — Translation-overlap / note-derived pairs

| Script | Purpose |
|--------|---------|
| `translation_overlap_migration.py` → `translation_overlap/migrate.js` | Spanish-translation overlap → basic related hints |
| Live mongosh (2026-07) | Extracted ~30 pairs from `～X:` note patterns (e.g. 中心 ↔ 中央, 変化 ↔ 変更, 東洋 ↔ 西洋) |

Skip pure compounds (`～～家`, `～～客`); keep nuanced / derived pairs.

---

## Data model reminders

```js
// DB-linked related word
{ wordId: ObjectId(...), type: "related"|"synonym"|"antonym", note: "", tags: ["formal"] }

// Text-only basic word (not a vocabulary entry)
{ word: "天気", type: "related", note: "", tags: ["casual"] }
```

- `related.wordId` is stored as **ObjectId** (use `ObjectId(...)` in arrayFilters).
- Nuance tags on Anki CSV appear as `(formal, spoken)` in `related_front` / `related_back`.
- Front masks shared kanji with `■`; back shows full words.

---

## Script index

### Status & analysis

| File | Role |
|------|------|
| `db_status_check.js` | Live JLPT relationship / tag counts |
| `analyze_relationships.py` | Snapshot relationship analysis |
| `analyze_nuances.py` | Nuance coverage analysis |

### N3 / shared early pipeline

| File | Role |
|------|------|
| `migrate_relationships.py` | Early relationship migration generator |
| `apply_nuance_tags.py` / `.js` | Apply N3-era nuance tags |
| `fix_relationship_errors.js` | Fix bad relationship entries |
| `n3_nuance_tags.py`, `n3_relationships.json` | N3 tag definitions & data |
| `relationship_analysis/` | Early extraction artifacts |

### N2 pipeline

| File | Role |
|------|------|
| `n2_analyze_state.py` | Pre-migration state |
| `n2_extract_relationships.py` | Resolve note refs → JSON |
| `n2_generate_migration.py` | Build mongosh ops |
| `n2_extract_pairs.py` | Pairs needing tags |
| `n2_nuance_tags.py` | Tag definitions |
| `n2_apply_nuance_tags.py` | Generate apply script |
| `n2_analysis/` | All N2 JSON + `.js` migrations |

### N1 pipeline

| File | Role |
|------|------|
| `n1_analyze_state.py` | Pre-migration state |
| `n1_extract_relationships.py` | Resolve note refs |
| `n1_extract_pairs.js` | Pairs for tagging |
| `n1_nuance_tags.py` / `n1_apply_nuance_tags.py` | Tags + apply generator |
| `n1_analysis/` | All N1 JSON + `.js` migrations |

### Cross-level nuance fill (2026-07)

| File | Role |
|------|------|
| `nuance_synonyms.py`, `nuance_antonyms.py` | Type-specific curation |
| `nuance_related_n{1,2,3}.py` | Related-type curation |
| `nuance_tags/` | Generated apply scripts + `curate_all*` |

### Enrichment

| File | Role |
|------|------|
| `basic_words_migration.py`, `basic_words/` | Text-only basic related words |
| `translation_overlap_migration.py`, `translation_overlap/` | Translation-based related hints |

---

## Conventions for future migrations

1. Prefer snapshot analysis first (`snapshots/*.json`), then generate mongosh — don’t hand-edit live docs at scale.
2. Always create **bidirectional** links for `wordId` relationships; never for basic `word` entries.
3. Tag swaps when reversing: `formal`↔`casual`, `spoken`↔`written`; keep `technical` / `literary` as appropriate.
4. Idempotent updates: only `$set` tags when `tags` is missing or empty.
5. Re-run `db_status_check.js` after each batch and update `.cursor/rules/data-migration-status.mdc`.
