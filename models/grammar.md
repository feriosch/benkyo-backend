# Grammar objects

## Clause
```ignorelang
{
    title: string
    (optional) hiragana: string
    translation: string
    level: string
    type: Type
    (optional) tags: Tags
    definition: string
    keys: [Example]
    formations: [Formation]
    (optional) examples: [Example]
    notes: [Section]
    (optional) related: [Related]
}
```

### Type
```ignorelang
{
    adjective: boolean
    adverb: boolean
    auxiliary: boolean
    conjunction: boolean
    modifier: boolean
    noun: boolean
    particle: boolean
    phrase: boolean
    structure: boolean
    suffix: boolean
}
```
### Tags
```ignorelang
{
    (optional) spoken: boolean
    (optional) written: boolean
    (optional) formal: boolean
    (optional) colloquial: boolean
    (optional) interrogative: boolean
}
```

### Example
```ignorelang
{
    [1] sentence: string
    translation: string
}
```

### Formation
```ignorelang
{
    [1] rule: string
    examples: [Example]
}
```

### Section
```ignorelang
{
    explanation: string
    (optional) examples: [Example]
}
```

### Related
```ignorelang
{
    title: string
    (optional) hiragana: string
    (optional) reference: string
    sections: [Section]
}
```


## Additional Notes
### [1] Sentence format
Sentences have the following format:

`かれが外国語を好んで*勉強している*_のは_、_一つには_、異文化学習が好んだ_からだ_。`

Where:
 - \*X* : X is a grammatical component (red).
 - \_X_ : X is a bold component.
 - \$X$ : X is an incorrect component.

The backend will split the sentences and give the corresponding list format according to the type 
to the front end.
- Example: `かれが外国語を好んで*勉強している*_のは_、_一つには_、異文化学習が好んだ_からだ_。`
```python
sentence = [
    'かれが外国語を好んで',
    'b/勉強している',
    'r/のは',
    '、',
    'r/一つには',
    '、異文化学習が好んだ',
    'r/からだ',
    '。'
]
```
