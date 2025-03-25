from dataclasses import dataclass, asdict
from datetime import datetime
from pymongo import MongoClient
import json
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()
mongo_uri = os.getenv("MONGODB_URI")
if not mongo_uri:
    raise ValueError("MONGODB_URI not set in environment variables")


# dataclass for user preferences
@dataclass
class UserPreferences:
    timezone: str


# dataclass for user
@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    active: bool = True
    created_ts: float


# function to parse user data from JSON
def parse_user_data(user_data):
    # create a list of roles based on user data
    roles = []
    if user_data.get("is_user_admin"):
        roles.append("admin")
    if user_data.get("is_user_manager"):
        roles.append("manager")
    if user_data.get("is_user_tester"):
        roles.append("tester")

    # return a User object with parsed data
    return User(
        username=user_data["user"],
        password=user_data["password"],
        roles=roles,
        preferences=UserPreferences(timezone=user_data["user_timezone"]),
        active=user_data["is_user_active"],
        created_ts=datetime.fromisoformat(
            user_data["created_at"].replace("Z", "")
        ).timestamp(),
    )


# mongoDB connection and import users
def import_users_to_mongodb(filename):
    # load JSON data
    with open(filename, "r") as f:
        data = json.load(f)

    # connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client["mydatabase"]
    users_collection = db["users"]

    # drop existing collection
    for user_data in data["users"]:
        user = parse_user_data(user_data)
        users_collection.insert_one(asdict(user))

    # print number of users imported
    print(f"Imported {len(data['users'])} users")

    # close the connection
    client.close()


# main function to run the script
if __name__ == "__main__":
    import_users_to_mongodb("udata.json")
