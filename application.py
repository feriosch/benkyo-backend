import os
from flask import (Flask, jsonify, make_response)
from flask_cors import CORS

from jap_dev.helpers.exceptions import BadRequestException, UnauthorizedException
from jap_dev.views.views import views


application = Flask(__name__)
CORS(application)


@application.route("/")
def status_check():
    return jsonify({'status': 'ok'})


def add_rule(route, view, methods):
    application.add_url_rule(
        route,
        view_func=view,
        methods=methods
    )


add_rule('/users', views['user']['main'], ['GET', 'POST'])
add_rule('/login', views['user']['login'], ['POST'])
add_rule('/session', views['user']['session'], ['GET'])

add_rule('/kanjis', views['kanji']['main'], ['GET', 'POST', 'PUT'])
add_rule('/kanjis/search', views['kanji']['search'], ['GET'])
add_rule('/kanjis/exists', views['kanji']['verify'], ['GET'])
add_rule('/kanjis/components', views['kanji']['components'], ['GET'])

add_rule('/collections', views['collection']['main'], ['GET', 'POST'])

add_rule('/words', views['word']['main'], ['GET', 'POST', 'PUT', 'DELETE'])
add_rule('/words/search', views['word']['search'], ['GET'])
add_rule('/words/level', views['word']['level'], ['PUT'])
add_rule('/words/csv', views['word']['csv'], ['GET'])

add_rule('/clauses', views['clause']['main'], ['GET', 'POST', 'PUT'])
add_rule('/clauses/search', views['clause']['search'], ['GET'])


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
        port = 80
    application.run(host='0.0.0.0', port=port)
