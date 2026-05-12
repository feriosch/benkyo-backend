from jap_dev.information import words

projections = {
    'word': {
        '$cond': {
            'if': {'$in': ['usually_kana', {'$ifNull': ['$tags', []]}]},
            'then': '$hiragana',
            'else': '$word'
        }
    },
    'hiragana': {
        '$cond': {
            'if': {'$in': ['usually_kana', {'$ifNull': ['$tags', []]}]},
            'then': '',
            'else': '$hiragana'
        }
    }
}


related_lookup = {
    '$lookup': {
        'from': 'words',
        'localField': 'related.wordId',
        'foreignField': '_id',
        'as': '_relatedWords',
        'pipeline': [{'$project': {'word': 1, 'hiragana': 1, 'group': 1}}]
    }
}


def get_words_for_csv(collection, tags, usually_kana):
    pipeline = []
    if collection:
        pipeline.append({'$match': {'group': collection}})
    if tags:
        pipeline.append({'$match': {'tags': {'$all': tags}}})
    pipeline.append(related_lookup)
    if usually_kana:
        word_projection = projections['word']
        hiragana_projection = projections['hiragana']
    else:
        word_projection = 1
        hiragana_projection = 1
    pipeline.append({
        '$project': {
            '_id': 0,
            'word': word_projection,
            'hiragana': hiragana_projection,
            'spanish': 1,
            'type': 1,
            'tags': 1,
            'sentence': {'$first': '$sentences.sentence'},
            'translation': {'$first': '$sentences.translation'},
            'notes': 1,
            'related': 1,
            '_relatedWords': 1
        }
    })
    return words().aggregate(pipeline)


def get_jlpt_words_for_csv(usually_kana):
    pipeline = [{
        '$match': {
            '$or': [
                {'group': 'jlpt_n3'},
                {'group': 'jlpt_n2'},
                {'group': 'jlpt_n1'},
                {'tags': {'$all': ['jlpt_n1']}}
            ]
        }
    }]
    pipeline.append(related_lookup)
    if usually_kana:
        word_projection = projections['word']
        hiragana_projection = projections['hiragana']
    else:
        word_projection = 1
        hiragana_projection = 1
    pipeline.append({
        '$project': {
            '_id': 0,
            'word': word_projection,
            'hiragana': hiragana_projection,
            'spanish': 1,
            'type': 1,
            'tags': 1,
            'sentence': {'$first': '$sentences.sentence'},
            'translation': {'$first': '$sentences.translation'},
            'notes': 1,
            'related': 1,
            '_relatedWords': 1
        }
    })
    return words().aggregate(pipeline)
