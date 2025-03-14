from pymongo import MongoClient
from app.settings import MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DB

URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
client = MongoClient(URI)
db = client[MONGO_DB]
client.admin.command('ping')


def get_db():
    return db

def get_collection(collection_name: str):
    return db[collection_name]
