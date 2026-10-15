---
name: export-csv
description: >-
  Export Benkyo vocabulary as an Anki CSV file and save it to a local folder. Use whenever the user asks for a CSV, a JLPT CSV, an Anki export or a deck file of their words (e.g. "give me the JLPT csv", "export gaming words to csv", "/export-csv jlpt"), even if they don't mention Anki or a folder.
argument-hint: '[jlpt | <group>] [tags…] [kanji] [output folder]'
---

# Export a word CSV for Anki

Input: `$ARGUMENTS`, or what the user asked for in the prompt.

The export runs `export_csv.py` (next to this file). It calls the same response functions as
`GET /words/csv` and `GET /words/csv/jlpt`, so the file is identical to the endpoint's, but it
needs neither the Flask server nor a login token. It is **read-only** (aggregations only), so
it needs no write approval.

## 1. Work out the options

| User asks for | Flag |
|---|---|
| "JLPT csv", "JLPT deck", "all JLPT words" | `--jlpt` (groups `jlpt_n3`, `jlpt_n2`, `jlpt_n1` + any word tagged `jlpt_n1`) |
| a group: anime, basic, gaming, jlpt_n1, jlpt_n2, jlpt_n3, literature, miscellaneous, movie | `--group <name>` |
| "all words", "everything", plain "csv" with no scope | no scope flag |
| only words with certain tags (`common`, `expression`, `rare`…), not with `--jlpt` | `--tag <tag>`, up to 3 |
| kanji form even for usually-kana words | `--no-kana` (default exports usually-kana words in kana) |
| a folder | `--out <dir>` (default `C:/Users/Boogs/Downloads/benkyo-anki`) |

If the request is a plain "CSV" and it's unclear whether they mean JLPT or everything, ask.
Tags are snake_case as stored in the DB (`usually_kana`, `jlpt_n1`…).

## 2. Run it

From the backend repo root (the worktree this skill was loaded from):

```bash
set -a; . /c/Users/Boogs/.benkyo/claude-db.env; set +a
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe .claude/skills/export-csv/export_csv.py --jlpt
```

- Never print or echo `MONGODB_URI`.
- If `.venv` is missing or lacks the dependencies, create it with
  `uv venv --python 3.11 .venv && uv pip install --python .venv/Scripts/python.exe -r requirements.txt`
  (`numpy 2.4` needs Python 3.11+; the system Python is 3.10).
- The export uses the CSV code of the **checked-out branch**. If the branch has unmerged
  changes to `*/word/csv.py`, say so, because the file may differ from what production returns.

The file is named `<scope>[-<tags>][-kanji]-<YYYY-MM-DD>.csv`, e.g. `jlpt-2026-10-15.csv`.
Exporting again on the same day overwrites that file.

## 3. Report

Give the full path and the note count the script prints. Then remind the user how to import
it in Anki (details in `anki/README.md`): File → Import, pick the Benkyo note type and deck,
and set **Existing notes** to **Update**. The file's header lines already set the separator,
HTML and the field mapping. Id is the key, so re-importing updates notes in place.

If the script says no words matched, say which filter was used and suggest dropping a tag or
checking the group name.
