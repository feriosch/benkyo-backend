import os
from flask import (Flask, jsonify, make_response)
from flask_cors import CORS

from jap_dev.helpers.exceptions import BadRequestException, UnauthorizedException
from jap_dev.views.user import User, Login
from jap_dev.views.kanji import Kanji
from jap_dev.views.group_collection import GroupCollection
from jap_dev.views.word import Word, SearchOne, SearchMany, UpdateLevel

application = Flask(__name__)
# Disable cross-origin check : Front and back not in same net.
CORS(application)


@application.route("/")
def status_check():
    return jsonify({'status': 'ok'})


user_view = User.as_view('user')
login_view = Login.as_view('login')
kanji_view = Kanji.as_view('kanjis')
group_collection_view = GroupCollection.as_view('groupcollection')
search_one_view = SearchOne.as_view('searchone')
search_many_view = SearchMany.as_view('searchmany')
update_word_level_view = UpdateLevel.as_view('updatewordlevel')
words_view = Word.as_view('words')

application.add_url_rule(
    '/users',
    view_func=user_view,
    methods=['GET', 'POST']
)

application.add_url_rule(
    '/login',
    view_func=login_view,
    methods=['POST']
)

application.add_url_rule(
    '/kanjis',
    view_func=kanji_view,
    methods=['GET', 'POST']
)

application.add_url_rule(
    '/groupcollections',
    view_func=group_collection_view,
    methods=['GET', 'POST']
)

application.add_url_rule(
    '/searchone',
    view_func=search_one_view,
    methods=['GET']
)

application.add_url_rule(
    '/searchmany',
    view_func=search_many_view,
    methods=['GET']
)

application.add_url_rule(
    '/updatewordlevel',
    view_func=update_word_level_view,
    methods=['PUT']
)

application.add_url_rule(
    '/words',
    view_func=words_view,
    methods=['GET', 'POST', 'PUT']
)


@application.errorhandler(BadRequestException)
def handle_bad_request(e):
    return make_response(jsonify({'error': e.message}), e.code)


@application.errorhandler(UnauthorizedException)
def handle_bad_request(e):
    return make_response(jsonify({'error': e.message}), e.code)


if __name__ == '__main__':
    try:
        port = os.getenv('PORT')
    except NameError:
        port = 5000
    application.run(host='0.0.0.0', port=port)
