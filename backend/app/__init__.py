from flask import Flask
from flask_cors import CORS
from .config import Config
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.database.database import get_collection
from app.api.users import users_blueprint, get_routes


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    app.config.from_object(Config)

    user_collection = get_collection()
    user_repository = UserRepository(user_collection)
    user_service = UserService(user_repository)
    user_routes = get_routes(user_service)

    app.register_blueprint(users_blueprint, url_prefix="/api")

    return app
