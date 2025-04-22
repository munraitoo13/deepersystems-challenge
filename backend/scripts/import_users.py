from dataclasses import asdict, dataclass
from datetime import datetime
import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")


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
    active: bool
    updatedAt: datetime | None = None


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
        createdAt=datetime.fromisoformat(user_data["created_at"]),
        active=user_data["is_user_active"],
        updatedAt=None,
    )


# mongoDB connection and import users
def import_users():
    # load json data
    with open("./scripts/udata.json", "r") as udata:
        data = json.load(udata)

    # connect to mongodb
    client = MongoClient(mongo_uri)
    db = client["mydatabase"]
    users_collection = db["users"]

    # insert users into mongodb
    users = [asdict(parse_users(user)) for user in data["users"]]
    users_collection.insert_many(users)

    # print number of users imported
    print(f"Imported {len(users)} users to MongoDB.")

    # close the connection
    client.close()


# main function to run the script
if __name__ == "__main__":
    import_users()
