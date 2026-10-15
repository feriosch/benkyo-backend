---
name: suggest-related
description: >-
  Check a related word the user thought of while studying a Benkyo/Anki card and add the relationship to the database if it holds, or explain why it doesn't. Use whenever the user names a word and another word it made them think of, or says a relation is missing (e.g. "for 待ち望む I was thinking 期待", "待ち望む reminds me of 期待", "is 杞憂 related to 心配?", "/suggest-related 待ち望む 期待"), even if they don't mention relations or the database.
argument-hint: '<card word> <word you thought of> [more words…]'
---

# Check and add a suggested related word

Input: `$ARGUMENTS`, or the user's message. It has the **card word** (the word being studied,
usually on a definition card) and one or more **suggested words** the user associated with it.
If it's unclear which word is which, ask.

The user is studying and wants a quick answer. Lead with the verdict, keep the rest short.

This skill relies on the `add-word` skill (`.claude/skills/add-word/SKILL.md`) for DB access,
the rules for relationship notes and tags (its step 5), adding new words, and the log format
(its step 8). Read it if it isn't loaded yet.

## 1. Look both words up

- **DB:** `db.words.find({$or:[{word:W},{hiragana:W}]})` for the card word and each
  suggestion. Note their `_id`, `spanish`, `group`, `tags` and existing `related` edges.
- **jisho.org:** meanings, JLPT level and `is_common` for both. The card word usually is in the
  DB; if it isn't, ask the user which word they mean.

## 2. Judge the association

Decide what the relationship really is, using jisho's meanings and your own knowledge of usage:

| Verdict | When | Action |
|---|---|---|
| **synonym** | same meaning; often interchangeable in context | add, `type: "synonym"` |
| **antonym** | opposite meaning | add, `type: "antonym"` |
| **related** | near-synonym with a clear difference in nuance, register or scope; same concept seen from another angle; or a common trap that's worth remembering together | add, `type: "related"` |
| **not related** | the user misremembered a meaning, the words only share a kanji (plain compounds), or they're too far apart to help | don't add; correct the user |

Tell the user plainly whether they were right. When they were partly right (e.g. they
thought "synonym" but it's only related), say what the difference is. When they were wrong,
correct them kindly: give both meanings, one short example sentence for each, and if a
better-fitting word exists (in the DB or not), suggest it.

## 3. If a suggested word isn't in the DB

- **N4/N5 or everyday basic word:** add it as a text-only hint on the card word only:
  `{ word: "天気", type, note, tags }` (no reverse link).
- **N3 and above:** add it as a new word following `add-word` steps 1–7, then link it. The
  user found it while studying their JLPT deck, so an N1 word goes to the `jlpt_n1` group
  (with the `jlpt_n1` tag). If it has no JLPT tag, ask which group it belongs to.

## 4. Write the links

Follow `add-word` step 5 for each edge:
- `note` is in English and describes how **the linked word** differs from the word holding
  the edge.
- `tags` say how the linked word is used compared to the other one (`formal`, `spoken`,
  `literary`…).
- Write **both directions**, with the reverse edge's tags swapped where they have an opposite
  (`formal`↔`casual`, `spoken`↔`written`).

Also check:
- **The link already exists:** don't duplicate it. Tell the user it's already there, and
  remind them the card only shows it after a new export (step 6). If its note or tags are
  weak, improve them.
- **The card word has few or no relations:** while you're there, add other clear missing
  synonyms/antonyms/related words from the DB (search by shared kanji and by overlapping
  `spanish`). Only clear ones, and list them separately in the report.

**Approval:** none needed for adding or improving links between existing words, or for adding
a new word that counts as a trivial add under `add-word` step 6. Ask first if you needed to ask
the user anything (meaning, homograph, group), or before removing or retyping an existing link.

Write with one `.js` file run through `mongosh --file`:
1. print a `BACKUP <EJSON>` line for every document you're about to change;
2. `updateOne({_id: SRC, "related.wordId": {$ne: TARGET}}, {$push: {related: EDGE}})` per edge,
   so re-running never duplicates a link (for text-only hints, check `related.word` instead);
3. print matched/modified counts per edge.

Then read the documents back and confirm the edges are there.

## 5. Log

Append to `/c/Users/Boogs/.benkyo/word-log.md` as in `add-word` step 8: one `edited` line for
the card word listing all links written (`related (user suggested <word>)` as the changed
fields), plus an `added` line for any new word. Use `auto` unless the user approved it.

## 6. Report

1. **Verdict:** right / partly right / not related, with the difference in one or two lines.
2. **Written:** each link as `card word → word (type, tags): note`, with the reverse links
   implied. List any extra links from step 4 separately.
3. **Anki:** the card shows the new relation after the next export. Offer to run
   `/export-csv` and remind the user to import with **Existing notes: Update**. The Id field
   keeps their review history.
