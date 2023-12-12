from pandas import DataFrame

from jap_dev.queries.word.csv import get_words_for_csv


def get_words_csv_response(params):
    collection = None
    file_name = 'benkyo'
    tags = []
    usually_kana = True

    if 'group' in params:
        collection = params['group']
        file_name = params['group']
    if 'tag_1' in params:
        tags.append(params['tag_1'])
    if 'tag_2' in params:
        tags.append(params['tag_2'])
    if 'tag_3' in params:
        tags.append(params['tag_3'])
    if 'usually_kana' in params:
        usually_kana = eval(str(params['usually_kana']).capitalize())
    df = DataFrame.from_dict(get_words_for_csv(collection, tags, usually_kana))
    df = df.reindex(columns=['word', 'hiragana', 'spanish', 'sentence', 'translation'])
    if not df.empty:
        df.to_csv(f'./files/{file_name}.csv', index=False, header=False)
        return file_name
    return False
