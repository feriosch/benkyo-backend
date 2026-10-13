---
name: add-word
description: Add a new Japanese vocabulary word or expression to the Benkyo MongoDB database (vocabulary.words), or review and improve it if it already exists. Use whenever the user says they found, learned, saw or want to add/save a Japanese word or expression (e.g. "new word: 囁く", "add 首にされる, I'm reading", "/add-word 懸賞"), even if they don't mention the database.
argument-hint: <word or expression> [what you were doing: reading, gaming, anime, movie, studying N1…]
---

# Add a word to Benkyo

Input: `$ARGUMENTS` — one or more Japanese words or expressions, plus optional context: what the user was doing when they found it (reading, gaming, watching anime, a movie, studying for JLPT N1…), which meaning they care about, where they saw it. If no word is given, ask for one.

DB access: `set -a; . /c/Users/Boogs/.benkyo/claude-db.env; set +a` then `mongosh "$MONGODB_URI"`. Database `vocabulary`, collection `words`. It is **production**: never print the URI or password, and never write before the user approves the draft (step 6).

For any mongosh call with Japanese text, write the script to a `.js` file in the scratchpad and run `mongosh "$MONGODB_URI" --quiet --file <file>`. Quoting Japanese inside `--eval` breaks easily.

## 1. Look it up

- **DB:** `db.words.find({$or:[{word:W},{hiragana:W}]})`. If it already exists, go to **Repeated words** below instead of stopping.
- **jisho.org:** `curl -s "https://jisho.org/api/v1/search/words?keyword=<url-encoded W>"`. Take the entry whose `slug` or `japanese[].word` matches. It gives the reading, `jlpt`, `is_common`, parts of speech, sense `tags` (Archaic, Rare, Colloquial, Female term, Slang, Kansai dialect…) and English meanings. If several homographs match, ask which one.

## 2. Pick the group (collection)

Use jisho's JLPT tag, then what the user was doing:

| jisho JLPT | group | extra tag |
|---|---|---|
| N2 | `jlpt_n2` (whatever the user was doing) | — |
| N3 | `jlpt_n3` (whatever the user was doing) | — |
| N4 / N5 | `basic` (whatever the user was doing) | — |
| N1 | the user's activity group, **or** `jlpt_n1` only if they were studying for JLPT N1 | `jlpt_n1` |
| none | the user's activity group | — |

Activity → group: reading (books, manga, articles) → `literature`, games → `gaming`, anime → `anime`, movies/dramas/series → `movie`, anything else → `miscellaneous`.

If the word is N1 or has no JLPT tag and the user didn't say what they were doing, ask. Never create `jlpt_n4`/`jlpt_n5` groups.

## 3. Expressions

An expression is a set phrase such as 首にされる or 腹が立つ. Store it as one word: `word: "首にされる"`, give it the `expression` tag, and use the `type` of what it acts as (`首にされる` → `verb`). Its group follows step 2, using the expression's own JLPT tag, which usually means the activity group.

Then look at its **main components** (首, する):

- **All components are basic or known** (N4/N5 on jisho, or already in the DB): add **only** the expression.
- **One or more components are unknown** (not in the DB and above N4): add **each unknown component as its own word** (full steps 1–5) **plus** the expression, and link them:
  - expression → component: `{type: "related", tags: ["component", …], note: "<what the component means on its own>"}`
  - component → expression: `{type: "related", tags: ["expression", …], note: "<what the expression means>"}`
- Also link the expression to any of its components that are already in the DB and not in `basic`, using the same tags.
- **Sentences:** the component word's example sentences must **not** use the expression. They should show the component used on its own. Usages of the expression go only in the expression's sentences.

If it's unclear whether the user knows a component, list your assumption in the draft so they can correct it.

## 4. Build the document

Match the shape of existing entries:

```js
{
  word: "囁く",                 // ALWAYS the kanji form if one exists (see "Kanji spelling" below)
  hiragana: "ささやく",
  spanish: "susurrar (a alguien, en voz baja)",   // SPANISH, short, comma-separated senses, context in parentheses
  type: { verb: 1 },            // keys: noun, suru, no_adj, na_adj, i_adj, adv, verb, adj_noun, adv_noun, counter (value 1)
  group: "jlpt_n2",
  tags: ["common", "usually_kana"],
  notes: "JLPT N2",             // "JLPT Nx" when jisho has a level; else a short Spanish note or omit
  sentences: [                  // 2 natural sentences at the word's level, with English translations
    { sentence: "彼は耳元で囁いた。", translation: "He whispered in my ear." }
  ],
  related: []                   // step 5
}
```

### Kanji spelling

If the word has a kanji spelling, store it in kanji. This holds however rare, obscure or unused that kanji is: `何処`, not `どこ`. Put the reading in `hiragana`. If jisho marks it "Usually written using kana alone", add the `usually_kana` tag; the Anki export then shows the kana form on the card. The user often types the kana form (どこ), so take the kanji spelling from jisho's `japanese[].word`, using the first one if there are several. Only words with no kanji spelling at all are stored in kana.

**Exception: kanji spellings shared by several readings.** Sometimes the exact same kanji spelling has more than one reading, e.g. `包む` is both つつむ and くるむ. Only the most common reading gets the kanji spelling: `包む` (つつむ). The other reading is stored in kana: `くるむ`. To find the most common reading:
- search jisho for the kanji spelling itself and compare the entries that use it;
- the reading of the top-ranked entry wins, and `is_common` breaks ties;
- if the DB already has that kanji spelling with another reading, the stored one is normally the common one.

State this choice in the draft, since the user may disagree. Example sentences should spell the word the way it's naturally written (usually kana for `usually_kana` words).

Type mapping from jisho parts of speech:
- Godan / Ichidan verbs → `verb`
- "Suru verb" → `noun` + `suru`
- "Na-adjective" → `na_adj`
- "No-adjective" → `no_adj`
- "I-adjective" → `i_adj`
- "Adverb" → `adv`
- "Adverb taking the 'to' particle" → `adv`, with `notes` set to `adv. と`
- "Counter" → `counter`

The `spanish` field drives the Anki definition card. It must tell this word apart from its near-synonyms, e.g. `premio (objeto)` vs `premio (dinero)`.

### Tags: when and how to use the word

Tags matter more and more. The user meets words they have never heard, and tags tell them **whether and when they should use the word**. Don't stop at the original basic tags: add every tag that would help.

**Basic tags** (the UI form knows these): `common`, `usually_kana`, `transitive`, `intransitive`, `expression`, `honorific`, `humble`, `onomatopoeic`, `jargon`, `ateji`, `joyogai`, `jlpt_n1`.

**Usage tags.** Add these when they apply, based on jisho sense tags and your own knowledge:
- Register: `formal`, `casual`, `polite`, `business`
- Medium: `written`, `spoken`, `literary`, `poetic`, `technical`
- Age and frequency: `archaic`, `obsolete`, `dated`, `rare`
- Social: `slang`, `internet_slang`, `vulgar`, `derogatory`, `euphemistic`
- Who uses it: `feminine`, `masculine`, `elderly_speech`, `youth_speech`, `childish`
- Dialect: `kansai_dialect` (and other `<region>_dialect`)
- Other: `idiomatic`, `yojijukugo`

You may invent a new tag when none of these captures something useful. Before inventing one:
- Check what already exists with `db.words.distinct("tags")` and `db.words.distinct("related.tags")`.
- Reuse an existing tag rather than adding a near-duplicate (`rare`, not `uncommon`).
- Keep tags lowercase snake_case English, one idea each.

Word-level usage tags show up on the Anki cards through the `Usage` field (the last CSV column). The UI edit form keeps them on save. Adding words through the UI is deprecated: this skill is now the way words get added.

## 5. Related words

Relationships, and their tags, are the user's most valuable study tool in Anki. Put real effort here.

Find candidates:
- words sharing a kanji: `{word: {$regex: "<kanji>"}}`
- words whose `spanish` overlaps this word's meaning
- jisho `see_also` and `antonyms`
- expression ↔ component links from step 3

For each real synonym, antonym, near-synonym, or expression/component link in the DB, add:

```js
{ wordId: ObjectId("..."), type: "synonym" | "antonym" | "related", note: "<English: how THAT word differs from this one>. N1", tags: [...] }
```

- `note` describes the **related** word's nuance, not the new word's. Write it in English and end it with that word's JLPT level (`N1`/`N2`/`N3`), or leave the level out if it has none.
- `tags` describe how the **related** word is used **compared to the new one**. Existing relationship tags are `formal`, `casual`, `spoken`, `written`, `technical`, `literary`, `polite`, `archaic`, `humble`. All the usage tags from step 4 are welcome too (`rare`, `feminine`, `elderly_speech`, `dated`…), as are `expression` and `component` from step 3. Anki shows these on both sides of the card. Be generous where a tag genuinely tells the two words apart.
- Links go **both ways**. For every link, plan the reverse `$push` on the other word, with its own note and with opposite tags swapped: `formal`↔`casual`, `spoken`↔`written`, `expression`↔`component`.
- Skip plain compounds that only contain the kanji (～家, ～客).
- An everyday N4/N5 word that isn't in the DB can be added as a text-only hint: `{ word: "天気", type: "related", note: "", tags: [] }`. Text-only hints get no reverse link.

## Repeated words

If the word is already in the DB, don't just skip it. Review the whole entry and propose improvements:
- Is the `spanish` field accurate, and does it tell the word apart from its synonyms?
- Are the type, group and tags right under the current rules? Add any missing usage tags.
- Is the word stored in kana even though it has a kanji spelling? Switch `word` to the kanji form and add `usually_kana` (see "Kanji spelling"), unless another, more common reading owns that kanji spelling.
- Are the sentences natural and at the right level? Does a component word use its own expression in its sentences?
- Is `notes` clean?
- Look for missing related words, missing reverse links, and weak or missing relationship notes and tags.

Show the proposal as a before → after diff. After approval, apply it with `updateOne` (`$set`, plus `$push` or arrayFilters for `related`).

## 6. Draft and approval

Show one compact draft covering all new words, expressions and edits:
- word, hiragana, spanish, type, group (and why), tags, notes, sentences
- each relationship, with both directions' notes and tags
- any assumptions (known/unknown components, the activity group)

Ask the user to approve or edit. Apply their edits, and show the draft again if anything changed substantially.

## 7. Write

Only after approval, write one `.js` file that:
1. inserts all new documents first and captures their `_id`s, so words in the same batch (such as an expression and its component) can link to each other;
2. sets the `related` arrays between the new words, and adds reverse links on existing words with `$push`, skipping any link that already exists;
3. applies the approved `$set` edits to existing words;
4. prints each new `_id` and the matched/modified counts.

Run it. Then read the affected documents back and tell the user what was written: the words, their `_id`s, the reverse links added and any edits. If anything failed, say exactly what was and wasn't written.
