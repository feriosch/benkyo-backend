from dotenv import load_dotenv
from google.cloud import storage
from flask import (jsonify, make_response)
import os

from jap_dev.helpers.exceptions import GeneralException
from jap_dev.queries.collection.verify import check_if_collection_exists
from jap_dev.queries.collection.main import insert_collection
from jap_dev.formatters.collection.insert import format_collection_insertion
from jap_dev.formatters.id.main import format_response_id

load_dotenv('.env')
bucket_name = os.getenv('BUCKET_NAME')


def insert_collection_response(collection):
    print(f'collection: ${collection}')
    if check_if_collection_exists(collection['collection_name']):
        return {'error': 'Repeated collection name'}, 400
    image_url = upload_collection_image(
        image_name=collection['image']['name'],
        image_path=collection['image']['path']
    )
    formatted_info = format_collection_insertion(collection, image_url)
    inserted_id = insert_collection(formatted_info)
    return jsonify(format_response_id(inserted_id))


def upload_collection_image(image_name, image_path):
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(image_name)
        blob.upload_from_filename(image_path)
        print(f"File {image_path} uploaded to {image_name}.")
        os.remove(image_path)
        return f'https://storage.googleapis.com/{bucket_name}/{image_name}'
    except GeneralException as error:
        return make_response(
            jsonify({'error': error.code}), 400
        )
