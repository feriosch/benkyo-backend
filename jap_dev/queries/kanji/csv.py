from jap_dev.information import kanjis


def get_kanji_for_csv():
    pipeline = [
        {'$sort': {'v1': 1}},
        {
            '$project': {
                '_id': 0,
                'kanji': 1,
                'spanish': 1,
                'on': 1,
                'kun': 1,
                'components': 1,
                'story': 1,
            }
        }
    ]
    return kanjis().aggregate(pipeline)
