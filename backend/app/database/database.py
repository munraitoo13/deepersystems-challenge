from pymongo import MongoClient
from app.config import Config

client = None


def get_client() -> MongoClient:
    global client
    if client is None:
        client = MongoClient(Config.MONGO_URI)

    return client


def get_database():
    client = get_client()
    return client["mydatabase"]


def get_collection():
    database = get_database()
    print(Config.MONGO_URI)
    return database["users"]
