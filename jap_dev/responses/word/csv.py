from pandas import DataFrame

from jap_dev.queries.word.csv import get_words_for_csv, get_jlpt_words_for_csv
from jap_dev.formatters.word.csv import format_all_csv_words

csv_columns = [
    'word', 'hiragana', 'spanish', 'type', 'notes', 'sentence', 'translation', 'common', 'jlpt_n1', 'expression',
    'onomatopoeic'
]


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
    words = get_words_for_csv(collection, tags, usually_kana)
    formatted_words = format_all_csv_words(words)
    df = DataFrame.from_dict(formatted_words)
    df = df.reindex(columns=csv_columns)
    if not df.empty:
        df.to_csv(f'./files/{file_name}.csv', index=False, header=False)
        return file_name
    return False


def get_jlpt_words_csv_response(params):
    usually_kana = True
    if 'usually_kana' in params:
        usually_kana = eval(str(params['usually_kana']).capitalize())
    words = get_jlpt_words_for_csv(usually_kana)
    formatted_words = format_all_csv_words(words)
    df = DataFrame.from_dict(formatted_words)
    df = df.reindex(columns=csv_columns)
    if not df.empty:
        df.to_csv(f'./files/jlpt.csv', index=False, header=False)
        return True
    return False
