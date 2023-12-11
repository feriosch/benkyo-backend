from jap_dev.information import words


def get_words_for_csv(collection=None, usually_kana=True):
    pipeline = []
    if collection:
        pipeline.append({'$match': {'group': collection}})
    if usually_kana:
        word_projection = {
            '$cond': {
                'if': {'$eq': ['$tags.usually_kana', True]},
                'then': '$hiragana',
                'else': '$word'
            }
        }
        hiragana_projection = {
            '$cond': {
                'if': {'$eq': ['$tags.usually_kana', True]},
                'then': '',
                'else': '$hiragana'
            }
        }
    else:
        word_projection = 1
        hiragana_projection = 1
    pipeline.append({
        '$project': {
            '_id': 0,
            'word': word_projection,
            'hiragana': hiragana_projection,
            'spanish': 1,
            'sentence': {'$first': '$sentences.sentence'},
            'translation': {'$first': '$sentences.translation'}
        }
    })
    return words().aggregate(pipeline)
