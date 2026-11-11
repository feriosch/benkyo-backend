# Benkyo Backend — rules for Claude

Flask 2.1 REST API + MongoDB Atlas for a personal Japanese-study app (vocabulary, kanji, grammar clauses, collections). Translations and notes are in **Spanish**. The companion UI is the Angular app at `E:/orca/benkyo/benkyo-ui` (see its `CLAUDE.md`); any API contract change must be mirrored there.

**The vocabulary has moved to Nando.** benkyo's `vocabulary` database now lives in Nando's Japanese Module as `japanese` (nando-server #36), and its Words are looked up, added and improved through the Nando Connector's Tools, with the `add-word` and `suggest-related` skills in nando-server (`skills/japanese/`). The copy left on benkyo's old cluster is stale and is to be deleted (nando-server #44). The rules below describe benkyo as it was.

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
- **Groups** follow the word's JLPT tag on **jisho.org**: N2 → `jlpt_n2`, N3 → `jlpt_n3`, N4/N5 → `basic`. N1 and untagged words go to the user's activity group (N1 also gets the `jlpt_n1` tag); the `jlpt_n1` group is only for words found while studying for N1. Untagged words already in `jlpt_n2` stay there. Gap-fill migrations put jisho N3 words that aren't already in the DB into `basic` (too basic to study). There are no N5/N4 collections: `basic` words exist so other words can link to them. Never create `jlpt_n4`/`jlpt_n5` groups. Adding words, and checking a related word the user thought of while studying, are now nando-server's `add-word` and `suggest-related` skills (`skills/japanese/`), through the Nando Connector.
- Tags are snake_case in the DB (`usually_kana`, `joyogai`, `jlpt_n1`…); the UI maps them to camelCase.

## Related words (core domain rules)

- DB-linked edge: `{wordId: ObjectId, type: related|synonym|antonym, note, tags?}`. **POST is bidirectional** and swaps tags on the reverse edge (`formal↔casual`, `spoken↔written`); `reverseNote` defaults to `note`.
- **PUT edits one side only** — no counterpart update, no tag swap. DELETE removes both sides.
- Basic (text-only) edge: `{word: "天気", type, note, tags?}` — never has a reverse link.
- Nuance tags: `formal, casual, spoken, written, literary, technical, archaic, polite, humble` — they describe how the *related* word differs from the source.
- `related.wordId` is stored as ObjectId — always wrap with `ObjectId(...)` in queries/arrayFilters.
- Anki export (`formatters/word/csv.py`): front masks shared kanji with `■`, back shows full words. The note type's templates and field list now live in nando-server (`internal/japanese/anki/`), next to its port of the JLPT export.

## Database access (retired)

Claude's own access to benkyo's database, the `claude-ai` Atlas user and its `claude-db.env` file on the user's PC, is retired with the move to Nando: the old cluster holds a stale copy, so write nothing to it. The user deletes the file when the cluster goes (nando-server #44). `scripts/README.md` keeps the history of the migrations run on it.

## Environment & commands

- Run locally: `python application.py` (reads `.env` via python-dotenv; `PORT` defaults to 80). Tests: `.venv/Scripts/python -m pytest` (pytest, `tests/`; install with `pip install -r requirements-dev.txt`). They cover the word CSV export only; the DB connection is stubbed in `tests/conftest.py`. The read-only integration test runs when `BENKYO_TEST_MONGODB_URI` is set. For other endpoints, verify with `curl` against the running server.
- Changes to the word CSV export (`*/word/csv.py`) must keep `python -m pytest` green; add tests for new behavior.
- Anki exports now come from Nando: the JLPT deck is `https://api.nanders.app/api/japanese/anki/jlpt.csv`, opened while signed in to Nando.
- Project targets Python 3.11+ (Docker uses 3.11-slim); the machine's default `python` is 3.10, so prefer a venv with 3.11+ if dependencies fail.
- `requirements.txt` is **UTF-16 LE** encoded — preserve the encoding when editing it.
- Deploy is a manual GitHub Actions `workflow_dispatch` (`.github/workflows/deploy.yml`) that pushes an image to GCP Artifact Registry. Never trigger it; the user does.
- Keep `README.md` API tables in sync when adding/changing endpoints.

## Git

- Work on feature branches; `master` is the main branch. Commit/push only when asked.
- Commit messages: short imperative summary, optional conventional prefix (`feat(csv):`, `style(anki):`) as in recent history.
