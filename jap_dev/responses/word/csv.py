from pandas import DataFrame

from jap_dev.queries.word.csv import get_words_for_csv, get_jlpt_words_for_csv
from jap_dev.formatters.word.csv import format_all_csv_words

csv_columns = [
    'id', 'word', 'hiragana', 'spanish', 'type', 'notes', 'sentence', 'translation', 'common', 'jlpt_n1', 'expression',
    'onomatopoeic', 'transitive', 'intransitive', 'related_front', 'related_back', 'usage'
]

# Anki note field names, in csv_columns order. Id is the first field, so Anki
# uses the word's ObjectId as the key when updating existing notes.
anki_fields = [
    'Id', 'Word', 'Pronunciation', 'Definition', 'Type', 'Notes', 'Japanese Sentence', 'Translation Sentence',
    'Common', 'JLPT N1', 'Expression', 'Onomatopoeic', 'Transitive', 'Intransitive', 'Related Front',
    'Related Back', 'Usage'
]

anki_header = (
    '#separator:Comma\n'
    '#html:true\n'
    f'#columns:{",".join(anki_fields)}\n'
)


def write_anki_csv(df, path):
    with open(path, 'w', encoding='utf-8', newline='') as file:
        file.write(anki_header)
        df.to_csv(file, index=False, header=False)


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
        write_anki_csv(df, f'./files/{file_name}.csv')
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
        write_anki_csv(df, './files/jlpt.csv')
        return True
    return False
