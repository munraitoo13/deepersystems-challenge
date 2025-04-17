from dataclasses import asdict
import json
from pymongo import MongoClient
from backend.scripts.utils import parse_users
from backend.config.env import mongo_uri


# mongoDB connection and import users
def import_users():
    # load json data
    with open("udata.json", "r") as users_file:
        data = json.load(users_file)

    # connect to mongodb
    client = MongoClient(mongo_uri)
    db = client["mydatabase"]
    users_collection = db["users"]

    # insert users into mongodb
    users_to_insert = [asdict(parse_users(user)) for user in data["users"]]
    users_collection.insert_many(users_to_insert)

    # print number of users imported
    print(f"Imported {len(users_to_insert)} users to MongoDB.")

    # close the connection
    client.close()
