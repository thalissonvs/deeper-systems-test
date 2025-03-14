from pymongo import MongoClient
from settings import MONGO_USERNAME, MONGO_PASSWORD, MONGO_HOST, MONGO_PORT, MONGO_DB

URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
print(URI)
client = MongoClient(URI)
db = client[MONGO_DB]

client.admin.command('ping')
print('db connected')

def get_db():
    return db

def get_collection(collection_name: str):
    return db[collection_name]
