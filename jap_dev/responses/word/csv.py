from pandas import DataFrame

from jap_dev.queries import word as queries


def get_words_csv_response(collection):
    df = DataFrame.from_dict(queries.get_words_for_csv(collection))
    df = df.reindex(columns=['word', 'hiragana', 'spanish', 'sentence', 'translation'])
    if not df.empty:
        if collection:
            df.to_csv(f'./files/{collection}.csv', index=False, header=False)
        else:
            df.to_csv('./files/benkyo.csv', index=False, header=False)
        return True
    return False
