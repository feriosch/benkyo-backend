"""Export a Benkyo word CSV for Anki without running the Flask server.

Calls the same response functions as GET /words/csv and GET /words/csv/jlpt, so the
file is identical to what the endpoints return. Read-only: it only runs aggregations.

Needs MONGODB_URI in the environment (load C:/Users/Boogs/.benkyo/claude-db.env first).
Never prints the URI.

    python export_csv.py --jlpt --out C:/Users/Boogs/Downloads/benkyo-anki
    python export_csv.py --group gaming --tag common --no-kana --out <dir>
"""
import argparse
import csv
import os
import shutil
import sys
import tempfile
import types
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUT = Path.home() / 'Downloads' / 'benkyo-anki'


def connect():
    uri = os.getenv('MONGODB_URI')
    if not uri:
        sys.exit('MONGODB_URI is not set. Load C:/Users/Boogs/.benkyo/claude-db.env first.')
    from pymongo import MongoClient
    client = MongoClient(uri, serverSelectionTimeoutMS=15000)
    # The app's own connection module reads DB_USERNAME/DB_PASSWORD from .env; swap
    # in this client so the export uses Claude's credentials instead.
    connection = types.ModuleType('jap_dev.helpers.connection')
    connection.database = client.get_default_database(default='vocabulary')
    sys.modules['jap_dev.helpers.connection'] = connection
    return client


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument('--jlpt', action='store_true', help='JLPT export (jlpt_n3/n2/n1 groups + jlpt_n1 tag)')
    scope.add_argument('--group', help='only this words.group (default: every word)')
    parser.add_argument('--tag', action='append', default=[], help='require this tag (up to 3, repeatable)')
    parser.add_argument('--no-kana', action='store_true', help='always export the kanji form (usually_kana=false)')
    parser.add_argument('--out', default=str(DEFAULT_OUT), help=f'output directory (default: {DEFAULT_OUT})')
    args = parser.parse_args()
    if args.jlpt and args.tag:
        parser.error('--tag only works with the regular export, not --jlpt')
    if len(args.tag) > 3:
        parser.error('at most 3 --tag values')

    sys.path.insert(0, str(REPO_ROOT))
    client = connect()
    import jap_dev.responses.word.csv as responses

    # Same string params the endpoints receive from the query string
    params = {'usually_kana': 'false' if args.no_kana else 'true'}
    if args.group:
        params['group'] = args.group
    for i, tag in enumerate(args.tag, start=1):
        params[f'tag_{i}'] = tag

    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as work:
        # The response functions write to ./files/<name>.csv
        os.chdir(work)
        os.mkdir('files')
        try:
            if args.jlpt:
                name = 'jlpt' if responses.get_jlpt_words_csv_response(params) else None
            else:
                name = responses.get_words_csv_response(params) or None
        finally:
            os.chdir(cwd)
            client.close()
        if not name:
            sys.exit('No words matched; nothing exported.')

        parts = [name, *args.tag, 'kanji' if args.no_kana else None, date.today().isoformat()]
        target = out_dir / ('-'.join(p for p in parts if p) + '.csv')
        shutil.move(os.path.join(work, 'files', f'{name}.csv'), target)

    with open(target, encoding='utf-8', newline='') as file:
        notes = sum(1 for row in csv.reader(file) if row and not row[0].startswith('#'))
    print(f'Wrote {target}')
    print(f'{notes} notes')


if __name__ == '__main__':
    main()
