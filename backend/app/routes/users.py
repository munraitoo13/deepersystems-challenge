from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

users_blueprint = Blueprint("users", __name__)


def get_routes(service: UserService):
    @users_blueprint.get("/users")
    def get_users():
        try:
            result = service.get_users()
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        return jsonify(result), 200 if result else (
            {"error": "No users found"},
            404,
        )

    @users_blueprint.get("/users/<user_id>")
    def get_user_by_id(user_id: str):
        result = service.get_user_by_id(user_id)
        return jsonify(result), 200 if result else ({"error": "User not found"}, 404)

    @users_blueprint.post("/users")
    def create_user():
        payload = request.json
        result = service.create_user(payload)
        return jsonify(result), 201 if result else jsonify(
            {"error": "User already exists"},
            400,
        )

    @users_blueprint.put("/users/<user_id>")
    def update_user(user_id: str):
        payload = request.json
        result = service.update_user(user_id, payload)
        return jsonify(result)

    @users_blueprint.delete("/users/<user_id>")
    def delete_user(user_id: str):
        result = service.delete_user(user_id)
        return jsonify(result)
