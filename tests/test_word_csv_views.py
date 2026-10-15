import pytest

import jap_dev.responses.word.csv as responses


@pytest.fixture
def one_word(monkeypatch):
    calls = []
    word = {'id': '64b000000000000000000001', 'word': '一層', 'hiragana': 'いっそう', 'spanish': 'aún más'}

    def get_words(collection, tags, usually_kana):
        calls.append((collection, tags, usually_kana))
        return iter([dict(word)])

    def get_jlpt_words(usually_kana):
        calls.append(usually_kana)
        return iter([dict(word)])

    monkeypatch.setattr(responses, 'get_words_for_csv', get_words)
    monkeypatch.setattr(responses, 'get_jlpt_words_for_csv', get_jlpt_words)
    return calls


@pytest.fixture
def no_words(monkeypatch):
    monkeypatch.setattr(responses, 'get_words_for_csv', lambda *args: iter([]))
    monkeypatch.setattr(responses, 'get_jlpt_words_for_csv', lambda *args: iter([]))


@pytest.mark.parametrize('url', ['/words/csv', '/words/csv/jlpt'])
def test_requires_session(client, one_word, url):
    response = client.get(url)
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Invalid session'}


@pytest.mark.parametrize('url', ['/words/csv', '/words/csv/jlpt'])
def test_rejects_invalid_token(client, one_word, url):
    response = client.get(url, headers={'Authorization': 'Bearer not-a-token'})
    assert response.status_code == 401


def test_words_csv_download(client, auth_header, one_word):
    response = client.get('/words/csv', headers=auth_header)
    assert response.status_code == 200
    assert 'attachment' in response.headers['Content-Disposition']
    assert 'benkyo.csv' in response.headers['Content-Disposition']
    body = response.get_data(as_text=True)
    assert body.startswith('#separator:Comma\n#html:true\n#columns:Id,Word,')
    assert '\n64b000000000000000000001,一層,いっそう,aún más,' in body


def test_words_csv_forwards_query_params(client, auth_header, one_word):
    response = client.get(
        '/words/csv?group=jlpt_n2&tag_1=common&tag_2=expression&usually_kana=false', headers=auth_header
    )
    assert response.status_code == 200
    assert 'jlpt_n2.csv' in response.headers['Content-Disposition']
    assert one_word == [('jlpt_n2', ['common', 'expression'], False)]


def test_jlpt_csv_download(client, auth_header, one_word):
    response = client.get('/words/csv/jlpt?usually_kana=false', headers=auth_header)
    assert response.status_code == 200
    assert 'jlpt.csv' in response.headers['Content-Disposition']
    assert '64b000000000000000000001' in response.get_data(as_text=True)
    assert one_word == [False]


@pytest.mark.parametrize('url', ['/words/csv', '/words/csv/jlpt'])
def test_empty_export_returns_error(client, auth_header, no_words, url):
    response = client.get(url, headers=auth_header)
    assert response.status_code == 500
    assert response.get_json() == {'error': 'Error processing CSV file.'}
