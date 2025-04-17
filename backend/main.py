from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from backend.config.env import mongo_uri
from backend.models.user_preferences import UserPreferences

# initialize flask app
app = Flask(__name__)
CORS(app)

# initialize mongo client
client = MongoClient(mongo_uri)

# initialize database
db = client["mydatabase"]
collection = db["users"]


# crud
# create user
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # validate required fields
    required_fields = ["username", "password", "roles"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    # Handle preferences separately
    preferences = data.get("preferences", {})
    user_preferences = UserPreferences(**preferences)

    # create User instance
    try:
        user = User(
            username=data["username"],
            password=data["password"],
            roles=data["roles"],
            preferences=user_preferences,
            active=data["active"],
        )
    except TypeError as e:
        return jsonify({"error": str(e)}), 400

    # convert to dictionary for insertion
    user_dict = user.__dict__.copy()
    user_dict["preferences"] = user.preferences.__dict__

    # Insert the user
    result = collection.insert_one(user_dict)
    user_dict["_id"] = str(result.inserted_id)

    return jsonify(user_dict), 201


# update user
@app.route("/api/users/<id>", methods=["PUT"])
def update_user(id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Prepare update dictionary
    update_data = {"updated_ts": datetime.now().timestamp()}

    # Update specific fields
    if "username" in data:
        update_data["username"] = data["username"]
    if "password" in data:
        update_data["password"] = data["password"]
    if "roles" in data:
        update_data["roles"] = data["roles"]
    if "preferences" in data:
        update_data["preferences"] = (
            UserPreferences(**data["preferences"]).__dict__
            if isinstance(data["preferences"], dict)
            else data["preferences"]
        )
    if "active" in data:
        update_data["active"] = data["active"]

    # Perform the update
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    if result.modified_count > 0:
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"error": "User not found or no changes made"}), 404


# get all users
@app.route("/api/users")
def get_users():
    users = list(collection.find())
    for user in users:
        user["_id"] = str(user["_id"])
    return jsonify(users)


# get user by id
@app.route("/api/users/<id>")
def get_user(id):
    user = collection.find_one({"_id": ObjectId(id)})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404


# delete user
@app.route("/api/users/<id>", methods=["DELETE"])
def delete_user(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "User deleted"}), 200
    else:
        return jsonify({"error": "User not found"}), 404


# run the app
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=7800)
