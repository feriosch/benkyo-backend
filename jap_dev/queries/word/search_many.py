from jap_dev.information import words


def search_many(word):
    return words().find({
        '$or': [
            {'word': {'$regex': '^' + word}},
            {'hiragana': {'$regex': '^' + word}},
            {'spanish': {'$regex': '^' + word}}
        ]
    })
