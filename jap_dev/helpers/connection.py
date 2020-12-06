from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
client_uri = 'mongodb+srv://{username}:{password}@cluster0.jtg6e.mongodb.net/{name}?retryWrites=true&w=majority'\
    .format(username=db_username, password=db_password, name=db_name)

client = MongoClient(client_uri)
database = client.get_database()


