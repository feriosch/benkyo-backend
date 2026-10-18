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

### Phase 6 — N3 gap fill against jisho.org (2026-10-12)

Compared every `jlpt_n3` word and its `notes` references with the jisho.org API (JLPT tags, see-also, antonyms). Words that are N5/N4/N3 on jisho but in none of the collections are too basic to study, so they went to `basic` as real vocabulary entries that other words can link to.

| File | Purpose |
|------|---------|
| `n3_gap_fill/SUMMARY.md` | Reviewed proposal: links by word, new basic words, notes cleanup |
| `n3_gap_fill/report.md` | Full analysis, including report-only items (JLPT mismatches, missing N2/N1 words) |
| `n3_gap_fill/curated_links.txt`, `new_basic.txt`, `nuance.txt` | Curated inputs |
| `n3_gap_fill/backup.js` → `snapshots/n3_gap_fill_backup.json` | Pre-migration copy of the 379 affected docs |
| `n3_gap_fill/migrate.js` | Idempotent apply script |

**Result:** 150 new `basic` words; 301 bidirectional links (602 edges; 110 with nuance tags); 189 `notes` stripped of references that are now real links (110 became empty). Re-run gave 0/0/0. Afterwards there were 0 dangling `wordId`s, and the 50 one-way edges were all there before this migration.

### Phase 7 — N2 gap fill against jisho.org (2026-10-13)

Same pipeline as Phase 6 for the existing `jlpt_n2` words. Related jisho N2/N1 words not in the DB were **not** added (listed as report-only). jisho N5/N4/N3 words not in any collection went to `basic`, stored in their kanji spelling with `usually_kana` where jisho says so (迚も, 瓦斯), per the `/add-word` skill. Relationship notes carry no JLPT suffix: the Anki badge shows the level.

| File | Purpose |
|------|---------|
| `n2_gap_fill/SUMMARY.md`, `report.md` | Reviewed proposal and full analysis (incl. 179 `jlpt_n2` words whose jisho tag isn't N2; the 38 untagged ones stay in N2) |
| `n2_gap_fill/curated.txt`, `new_basic.txt` | Curated links (with tags and notes for both sides) and new basic words |
| `n2_gap_fill/backup.js` → `snapshots/n2_gap_fill_backup.json` | Pre-migration copy of the 219 affected docs |
| `n2_gap_fill/migrate.js` | Idempotent apply script |

**Result:** 50 new `basic` words; 154 bidirectional links (308 edges; 30 with nuance tags); 63 `notes` cleaned (43 became empty). Re-run gave 0/0/0; 0 dangling `wordId`s; one-way edges unchanged at 50 (pre-existing). `jlpt_n2` words with related words: 505 / 1378.

### Phase 8 — Optional-と adverbs (2026-10-15)

`type.adv: 4` (UI shows ～と) had been used for every adverb jisho tags "taking と", although と is optional for most mimetics (ほんのり(と), じわじわ(と)). Rule now in the `/add-word` skill: optional と → `adv: 1` + note `adv. と`; `adv: 4` only when と is required (～たる kango like 敢然, 堂々; ぽかん, きょとん, 一段と…).

| File | Purpose |
|------|---------|
| `adv_to_optional_migration.js` | Hand-curated word lists; `var DRY=true` writes `snapshots/adv_to_optional_2026-10-14.json`, `DRY=false` applies (filtered on `type.adv: 4`, idempotent) |

**Result:** 52 modified: 43 → `adv: 1` + `adv. と` note, 8 with と built into the word (ぎゅっと, 真逆…) → `adv: 1`, まじまじと見る lost its stray `adv`. 57 words keep `adv: 4`.

### Phase 9 — Spanish parentheses that revealed the answer (2026-10-18)

The Anki definition card shows `spanish` on its front. 14 JLPT words had Japanese examples in parentheses there that contained the word itself (厳重: `… (厳重注意, 厳重な警備)`). Per the rule that `spanish` stays short, the parentheses moved to `notes`, which the export now masks on the front (`Notes Front`). Applied inline with targeted `$set` on `spanish`/`notes`, filtered on the old `spanish` value; no script kept.

| File | Purpose |
|------|---------|
| `snapshots/2026-10-18-spanish-parens-to-notes.json` | Pre-change copy of the 14 docs |

**Result:** 14 modified (尽くす only lost the parentheses: its notes already covered them). JLPT definitions containing the word, its reading or one of its kanji: 14 → 0. Each edit is in `word-log.md`.

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
