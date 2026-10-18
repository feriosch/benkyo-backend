---
name: add-word
description: >-
  Add a new Japanese vocabulary word or expression to the Benkyo MongoDB database (vocabulary.words), or review and improve it if it already exists. Use whenever the user says they found, learned, saw or want to add/save a Japanese word or expression (e.g. "new word: 囁く", "add 首にされる, I'm reading", "/add-word 懸賞"), even if they don't mention the database.
argument-hint: '<word or expression> [what you were doing: reading, gaming, anime, movie, studying N1…]'
---

# Add a word to Benkyo

Input: `$ARGUMENTS` — one or more Japanese words or expressions, plus optional context: what the user was doing when they found it (reading, gaming, watching anime, a movie, studying for JLPT N1…), which meaning they care about, where they saw it. If no word is given, ask for one.

DB access: `set -a; . /c/Users/Boogs/.benkyo/claude-db.env; set +a` then `mongosh "$MONGODB_URI"`. Database `vocabulary`, collection `words`. It is **production**: never print the URI or password, and only write without approval when step 6 allows it (new words and improvements to existing words; not deletes, merges, group moves or bulk changes). Every write is logged (step 8).

For any mongosh call with Japanese text, write the script to a `.js` file in the scratchpad and run `mongosh "$MONGODB_URI" --quiet --file <file>`. Quoting Japanese inside `--eval` breaks easily.

## 1. Look it up

- **DB:** `db.words.find({$or:[{word:W},{hiragana:W}]})`. If it already exists, go to **Repeated words** below instead of stopping.
- **jisho.org:** `curl -s "https://jisho.org/api/v1/search/words?keyword=<url-encoded W>"`. Take the entry whose `slug` or `japanese[].word` matches. It gives the reading, `jlpt`, `is_common`, parts of speech, sense `tags` (Archaic, Rare, Colloquial, Female term, Slang, Kansai dialect…) and English meanings. If several homographs match, ask which one.
- **Conjugations:** if the input is just a regular conjugation of a basic or known word (causative 死なせる ← 死ぬ, passive, potential, causative-passive…), don't add it, even when jisho lists it as its own entry. Tell the user which word it comes from and move on.
- **Conjugated input from a picture or screenshot:** if the user sends a picture of a conjugated verb or adjective (e.g. 震撼させる), write the **dictionary form** only. Never write the conjugated form anywhere, not in `word`, `notes`, `spanish`, or a link note, unless it is almost exclusive to an expression (e.g. 身を翻す, 屈託のない). The user already knows the conjugation rules; don't spell them out. Conjugated forms are fine inside notes or link notes when they are part of an expression or an example (e.g. 世界を震撼させる, 気絶させる as an example of use).

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

- **Confirm with jisho first.** The user often sends a phrase without knowing whether it's an expression. Look it up on jisho: if jisho lists it as an entry (e.g. 身を翻す, 色気より食い気, 屈託のない), store it as an expression. If jisho doesn't list it (e.g. 難問に直面する), it's just a common collocation: don't add it as its own word. Write the phrase as a note on the word(s) it's built from, in the form "X に Y する: <meaning> (collocación común)".

An expression is a set phrase such as 首にされる or 腹が立つ. Store it as one word: `word: "首にされる"`, give it the `expression` tag, and use the `type` of what it acts as (`首にされる` → `verb`). Its group follows step 2, using the expression's own JLPT tag, which usually means the activity group.

Then look at its **main components** (首, する):

- **All components are basic or known** (N4/N5 on jisho, or already in the DB): add **only** the expression.
- **One or more components are unknown** (not in the DB and above N4): add **each unknown component as its own word** (full steps 1–5) **plus** the expression, and link them:
  - expression → component: `{type: "related", tags: ["component", …], note: "<what the component means on its own>"}`
  - component → expression: `{type: "related", tags: ["expression", …], note: "<what the expression means>"}`
  - **Exception: components that barely live outside the compound.** If an unknown component is rarely used on its own and almost only appears in this expression or compound (通牒 → 最後通牒, 屈託 → 屈託のない), don't add it as a word: store only the expression/compound and explain the component in its `notes` (e.g. `屈託: preocupacion (casi solo se usa en esta expresion)`). The user doesn't want useless standalone entries. Mention the choice afterwards so they can ask for the component if they want it.
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

Spelling follows jisho: when jisho's headword is kana (e.g. ぱちり, こそばゆい, which jisho lists only in kana), store that kana as `word` and `hiragana`, even if the word is usually written in katakana in games or manga. Don't convert it to katakana.

Type values: the number is the form the UI shows, not a count. `1`/`2` = plain, `3` = ～に, `4` = ～と, `5` = ～的, `6` = ～的に, `7` = ～たる, `8` = ～を. E.g. 根本 is `{noun: 1, na_adj: 5, adv: 6}` (根本的, 根本的に).

Type mapping from jisho parts of speech:
- Godan / Ichidan verbs → `verb`
- "Suru verb" → `noun` + `suru`
- "Na-adjective" → `na_adj`
- "No-adjective" → `no_adj`
- "I-adjective" → `i_adj`
- "Adverb" → `adv`
- "Adverb taking the 'to' particle" → `adv: 1`, with `notes` set to `adv. と`. jisho's tag means と is *allowed*, not required: most mimetic adverbs work with or without it (ほんのり甘い / ほんのりと甘い, じわじわ, じっくり, うっすら). Use `adv: 4` (～と) only when と is required for adverbial use, which is mostly ～たる kango (敢然と, 堂々と, 颯爽と: ✗敢然立ち向かう).
- "Counter" → `counter`

The `spanish` field drives the Anki definition card. It must tell this word apart from its near-synonyms, e.g. `premio (objeto)` vs `premio (dinero)`.

### Tags: when and how to use the word

Tags matter more and more. The user meets words they have never heard, and tags tell them **whether and when they should use the word**. Don't stop at the original basic tags: add every tag that would help.

**Basic tags** (the UI form knows these): `common`, `usually_kana`, `transitive`, `intransitive`, `expression`, `honorific`, `humble`, `onomatopoeic`, `jargon`, `ateji`, `joyogai`, `jlpt_n1`.

**Jōyō check (required for every write):** first check each kanji in the headword against the DB `kanjis` collection (`db.kanjis.findOne({kanji: K})`). A kanji that is not in that collection is not jōyō, so add the `joyogai` tag (e.g. 捏 in 捏造, 嘔 in 嘔吐). If it is in the collection, it is still not certain to be jōyō (the collection has about 2,190 kanji, more than the 2,136 jōyō), so check it on `https://kanjiapi.dev/v1/kanji/<url-encoded kanji>` when the answer matters: `grade` null or 9+ means not jōyō. A response without a `grade` key is an error (rate limit): wait and retry, don't treat it as non-jōyō. Pace requests (about one per second).

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
{ wordId: ObjectId("..."), type: "synonym" | "antonym" | "related", note: "<English: how THAT word differs from this one>", tags: [...] }
```

- `note` describes the **related** word's nuance, not the new word's. Write it in English. Don't add the JLPT level: the Anki card shows it as a badge next to the related word.
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

Apply the improvements directly with `updateOne` (`$set`, plus `$push` or arrayFilters for `related`); no approval needed (see step 6). Print a `BACKUP` EJSON line of the doc before writing, then show the user a before → after diff of what changed.

## 6. Draft and approval

**Most writes need no approval.** Go straight to step 7 and show the user what was written afterwards when:
- you didn't need to ask the user anything (group, homograph, meaning, which reading gets the kanji, known/unknown components);
- the changes are new words, reverse `related` links, and/or **improvements to existing words** (the **Repeated words** review: spanish, type, tags, notes, sentences, reading/spelling fixes, related links and their notes/tags). The user trusts these judgment calls (2026-10-15).

Still ask first for: deleting a word, merging or splitting entries (e.g. 大家 おおや/たいか), moving a word to another group, and any bulk change across many words (that also follows the CLAUDE.md migration rules: snapshot, dry-run count, approval of the exact command).

Anything that needs approval: Show one compact draft covering all new words, expressions and edits:
- word, hiragana, spanish, type, group (and why), tags, notes, sentences
- each relationship, with both directions' notes and tags
- any assumptions (known/unknown components, the activity group)

Ask the user to approve or edit. Apply their edits, and show the draft again if anything changed substantially.

## 7. Write

**Concurrency (several chats may write to the DB at once):**
- Re-check that a new word doesn't exist in the same script, right before `insertOne`. An earlier check in the chat can be stale.
- For existing words, use targeted updates: `$push` for links and `$set` on only the fields you're changing. Don't overwrite a whole entry you read earlier, because another chat may have changed it since.
- Only one chat edits this skill file at a time. Other chats leave it alone.
- The word log is append-only. Don't rewrite it.

Straight away (or after approval, when step 6 requires it), write one `.js` file that:
1. inserts all new documents first and captures their `_id`s, so words in the same batch (such as an expression and its component) can link to each other;
2. sets the `related` arrays between the new words, and adds reverse links on existing words with `$push`, skipping any link that already exists;
3. applies the approved `$set` edits to existing words;
4. prints each new `_id` and the matched/modified counts.

Run it. Then read the affected documents back and tell the user what was written: the words, their `_id`s, the reverse links added and any edits. If anything failed, say exactly what was and wasn't written.

## 8. Log

After every write, approved or not, append one line per written word to `/c/Users/Boogs/.benkyo/word-log.md` (create it if missing, with a `# Benkyo word log` heading). Format:

```
- 2026-10-13 · added · 囁く (ささやく) · jlpt_n2 · 6a54f30739c7ab59a78cb305 · auto · rel: ~呟く(spoken), =小声で話す
```

- action: `added` or `edited` (for edits, list the changed fields instead of the group);
- `auto` for trivial adds, `approved` otherwise;
- `rel:` lists the relationships written, as type prefix (`=` synonym, `✕` antonym, `~` related) + word + tags; reverse links are implied.

Keep the line short. If a write failed, log only what actually reached the DB.
