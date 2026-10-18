# Anki note type

Templates for the CSV produced by `GET /words/csv` and `GET /words/csv/jlpt`.

| File | Where it goes in Anki |
|---|---|
| `styling.css` | Note type → Cards → Styling (shared by both card types) |
| `definition_card/front.html`, `back.html` | Card type 1: Definition → Word |
| `word_card/front.html`, `back.html` | Card type 2: Word → Definition |

## Fields

Create the note type with exactly these fields, in this order:

1. Id
2. Word
3. Pronunciation
4. Definition
5. Type
6. Notes
7. Japanese Sentence
8. Translation Sentence
9. Common
10. JLPT N1
11. Expression
12. Onomatopoeic
13. Transitive
14. Intransitive
15. Related Front
16. Related Back
17. Usage
18. Notes Front

`Notes Front` is `Notes` with the answer hidden (`■`): the word, its reading in
hiragana/katakana and any shared kanji. The definition card's front shows it; its back
shows the full `Notes`.

`Id` is the word's MongoDB ObjectId. It is the first field, so Anki uses it as the
note key: re-importing updates the existing note even if the word, its reading or
the `usually_kana` export option changed. No template shows it.

## Importing

The CSV starts with Anki header lines (`#separator`, `#html`, `#columns`), so the
import dialog picks the right separator, enables HTML and maps columns to fields by
name. Choose the note type and deck, and set **Existing notes** to **Update**.
