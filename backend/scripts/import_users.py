from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()
mongo_uri = os.getenv("MONGODB_URI")
if not mongo_uri:
    raise ValueError("MONGODB_URI environment variable not set")


# dataclass for user preferences
@dataclass
class UserPreferences:
    timezone: str


# dataclass for user
@dataclass
class User:
    username: str
    password: str
    roles: list[str]
    preferences: UserPreferences
    createdAt: datetime
    updatedAt: datetime | None
    active: bool


# function to parse user data from json
def parse_users(user_data):
    # create a list of roles based on user data
    roles = []
    if user_data.get("is_user_admin"):
        roles.append("admin")
    if user_data.get("is_user_manager"):
        roles.append("manager")
    if user_data.get("is_user_tester"):
        roles.append("tester")

    # return a user object with parsed data
    return User(
        username=user_data["user"],
        password=user_data["password"],
        roles=roles,
        preferences=UserPreferences(timezone=user_data["user_timezone"]),
        active=user_data["is_user_active"],
        createdAt=datetime.fromisoformat(
            user_data["created_at"].replace("Z", "")
        ).replace(tzinfo=timezone.utc),
        updatedAt=None,
    )


# mongoDB connection and import users
def import_users():
    # load json data
    with open("./scripts/udata.json", "r") as users_file:
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


# main function to run the script
if __name__ == "__main__":
    import_users()
