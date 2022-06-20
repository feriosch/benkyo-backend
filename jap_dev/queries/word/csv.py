from jap_dev.information import words


def get_words_for_csv(collection=None):
    pipeline = []
    if collection:
        pipeline.append({'$match': {'from': collection}})
    pipeline.append({
        '$project': {
            '_id': 0,
            'word': 1,
            'hiragana': 1,
            'spanish': 1,
            'sentence': {'$first': '$sentences.sentence'},
            'translation': {'$first': '$sentences.translation'}
        }
    })
    return words().aggregate(pipeline)
