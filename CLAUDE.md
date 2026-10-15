# Benkyo Backend — rules for Claude

Flask 2.1 REST API + MongoDB Atlas for a personal Japanese-study app (vocabulary, kanji, grammar clauses, collections). Translations and notes are in **Spanish**. The companion UI is the Angular app at `E:/orca/benkyo/benkyo-ui` (see its `CLAUDE.md`); any API contract change must be mirrored there.

## Architecture (follow this layering for every endpoint)

`application.py` registers routes → `jap_dev/views/views.py` maps names to `MethodView`s →

| Layer | Folder | Role |
|---|---|---|
| View | `jap_dev/views/<entity>/` | `MethodView`; `decorators = [validate_session]`; each method wrapped in `@validate_schema(...)`; returns `make_response(<response fn>(params))` |
| Schema | `jap_dev/schemas/<entity>/main/{get,insert,update,delete}.py` | `schema` lib validation, `error='<field> error'` messages |
| Response | `jap_dev/responses/<entity>/` | business logic; returns dict or `({'error': msg}, 400)` tuple |
| Query | `jap_dev/queries/<entity>/` | all Mongo access, via collection accessors in `jap_dev/information.py` |
| Formatter | `jap_dev/formatters/<entity>/` | DB doc ↔ API shape; `ObjectId` → `str` via `formatters/id` |

- Errors are `{"error": "..."}`; raise `BadRequestException` / `UnauthorizedException` (`jap_dev/helpers/exceptions.py`) or return the tuple.
- `jap_dev/views/word/related.py` is an exception that talks to the DB directly — fine to keep, don't spread the pattern.
- Mongo collections: `words`, `kanjis`, `clauses`, `group_collections`, `users`, `kanjiIrregularComponents`. `words.group` values: `anime, basic, gaming, jlpt_n1, jlpt_n2, jlpt_n3, literature, miscellaneous, movie` (`all` is a query sentinel, never stored).
- **Groups** follow the word's JLPT tag on **jisho.org**: N2 → `jlpt_n2`, N3 → `jlpt_n3`, N4/N5 → `basic`. N1 and untagged words go to the user's activity group (N1 also gets the `jlpt_n1` tag); the `jlpt_n1` group is only for words found while studying for N1. Untagged words already in `jlpt_n2` stay there. Gap-fill migrations put jisho N3 words that aren't already in the DB into `basic` (too basic to study). There are no N5/N4 collections: `basic` words exist so other words can link to them. Never create `jlpt_n4`/`jlpt_n5` groups. The full procedure for adding words is the `/add-word` skill (`.claude/skills/add-word/SKILL.md`).
- Tags are snake_case in the DB (`usually_kana`, `joyogai`, `jlpt_n1`…); the UI maps them to camelCase.

## Related words (core domain rules)

- DB-linked edge: `{wordId: ObjectId, type: related|synonym|antonym, note, tags?}`. **POST is bidirectional** and swaps tags on the reverse edge (`formal↔casual`, `spoken↔written`); `reverseNote` defaults to `note`.
- **PUT edits one side only** — no counterpart update, no tag swap. DELETE removes both sides.
- Basic (text-only) edge: `{word: "天気", type, note, tags?}` — never has a reverse link.
- Nuance tags: `formal, casual, spoken, written, literary, technical, archaic, polite, humble` — they describe how the *related* word differs from the source.
- `related.wordId` is stored as ObjectId — always wrap with `ObjectId(...)` in queries/arrayFilters.
- Anki export (`formatters/word/csv.py`, `anki/*/`): front masks shared kanji with `■`, back shows full words.

## Database access (PRODUCTION — there is no separate dev DB)

- Claude's own credentials live **outside the repo** in `C:\Users\Boogs\.benkyo\claude-db.env` (Atlas user `claude-ai`, read/write). Load with
  `set -a; . /c/Users/Boogs/.benkyo/claude-db.env; set +a` then `mongosh "$MONGODB_URI" ...`.
- Never print, echo, log, or commit the password/URI; never copy it into the repo, `.env`, scripts, or docs. The app's own `.env` belongs to the user — don't edit it.
- **Reads are free; writes need explicit user confirmation** (show the filter, the update, and the affected count from a dry-run `countDocuments` first). Never `drop`, `deleteMany`, or unfiltered `updateMany` without the user approving that exact command.
- Before any bulk migration: export the affected docs to `snapshots/` (gitignored) so it can be reverted; make updates idempotent; re-run `scripts/db_status_check.js` afterwards.
- Migration scripts go in `scripts/` (gitignored except `scripts/README.md`); update `scripts/README.md` timeline when a migration is done. Conventions are listed at the bottom of that README.

## Environment & commands

- Run locally: `python application.py` (reads `.env` via python-dotenv; `PORT` defaults to 80). Tests: `.venv/Scripts/python -m pytest` (pytest, `tests/`; install with `pip install -r requirements-dev.txt`). They cover the word CSV export only; the DB connection is stubbed in `tests/conftest.py`. The read-only integration test runs when `BENKYO_TEST_MONGODB_URI` is set (`BENKYO_TEST_MONGODB_URI="$MONGODB_URI"` after loading the claude env file). For other endpoints, verify with `curl` against the running server or with mongosh reads.
- Changes to the word CSV export (`*/word/csv.py`, `anki/`) must keep `python -m pytest` green; add tests for new behavior.
- Exporting a word CSV for Anki ("JLPT csv", "export gaming words") is the `/export-csv` skill (`.claude/skills/export-csv/`): it runs the endpoint's response code directly with Claude's read-only DB access and saves to `C:/Users/Boogs/Downloads/benkyo-anki` by default.
- Project targets Python 3.11+ (Docker uses 3.11-slim); the machine's default `python` is 3.10, so prefer a venv with 3.11+ if dependencies fail.
- `requirements.txt` is **UTF-16 LE** encoded — preserve the encoding when editing it.
- Deploy is a manual GitHub Actions `workflow_dispatch` (`.github/workflows/deploy.yml`) that pushes an image to GCP Artifact Registry. Never trigger it; the user does.
- Keep `README.md` API tables in sync when adding/changing endpoints.

## Git

- Work on feature branches; `master` is the main branch. Commit/push only when asked.
- Commit messages: short imperative summary, optional conventional prefix (`feat(csv):`, `style(anki):`) as in recent history.
