from flask import request, make_response, jsonify
from werkzeug.utils import secure_filename
from schema import SchemaError

from jap_dev.helpers.exceptions import GeneralException

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMAGE_DIRECTORY = './files/images'


def allowed_image_type(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image():
    try:
        image = request.files.get('image')
        if not allowed_image_type(image.filename):
            raise SchemaError('Extension not supported.')
        image_name = secure_filename(image.filename)
        image_path = '{path}/{name}'.format(path=IMAGE_DIRECTORY, name=image_name)
        image.save(image_path)
        return {
            'name': image_name,
            'path': image_path,
        }
    except GeneralException as error:
        return make_response(
            jsonify({'error': error.code}), 400
        )
