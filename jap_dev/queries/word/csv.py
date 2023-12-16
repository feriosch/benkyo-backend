from jap_dev.information import words

projections = {
    'word': {
        '$cond': {
            'if': {'$eq': ['$tags.usually_kana', True]},
            'then': '$hiragana',
            'else': '$word'
        }
    },
    'hiragana': {
        '$cond': {
            'if': {'$eq': ['$tags.usually_kana', True]},
            'then': '',
            'else': '$hiragana'
        }
    }
}


def get_words_for_csv(collection, tags, usually_kana):
    pipeline = []
    if collection:
        pipeline.append({'$match': {'group': collection}})
    if tags:
        pipeline.append({'$match': {'tags': {'$all': tags}}})
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
            'tags': 1,
            'sentence': {'$first': '$sentences.sentence'},
            'translation': {'$first': '$sentences.translation'}
        }
    })
    return words().aggregate(pipeline)


def get_jlpt_words_for_csv(usually_kana):
    pipeline = [{
        '$match': {
            '$or': [
                {'group': 'jlpt_n2'},
                {'group': 'jlpt_n1'},
                {'tags.jlpt_n1': True}
            ]
        }
    }]
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
            'tags': 1,
            'sentence': {'$first': '$sentences.sentence'},
            'translation': {'$first': '$sentences.translation'}
        }
    })
    return words().aggregate(pipeline)
