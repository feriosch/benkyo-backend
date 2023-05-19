from pandas import DataFrame

from jap_dev.queries.kanji.csv import get_kanji_for_csv
from jap_dev.formatters.kanji.csv import format_all_csv_kanjis


def get_kanjis_csv_response():
    kanjis = format_all_csv_kanjis(get_kanji_for_csv())
    df = DataFrame.from_dict(kanjis)
    df = df.reindex(columns=['kanji', 'spanish', 'on', 'kun', 'components', 'story'])
    if not df.empty:
        df.to_csv('./files/kanji.csv', index=False, header=False)
        return True
    return False
