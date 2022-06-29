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
    keys: [Key]
    formations: [Formation]
    examples: [Example]
    notes: [Note]
    related: [Related]
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

### Key
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

### Example
```ignorelang
{
    [1] sentence: string
    translation: string
}
```

### Note
```ignorelang
{
    sections: [Section]
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

### Section
```ignorelang
{
    explanation: string
    (optional) examples: [Example]
}
```

## Additional Notes
### [1] Sentence formaasst
Sentences have the following format:

`かれが外国語を好んで*勉強している*_のは_、_一つには_、異文化学習が好んだ_からだ_。`

Where:
 - \*X* : X is the highlighted grammar.
 - \_X_ : X is a bold component.
 - \$X$ : X is incorrect

The front end will split the sentences and give the corresponding format according to the type.
