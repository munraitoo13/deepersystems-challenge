from datetime import datetime, timezone
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.dtos.user_dto import UpdateUserDTO, CreateUserDTO
from bson import ObjectId


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_users(self) -> list[User]:
        users = self.repository.find_all()
        for user in users:
            user["_id"] = str(user["_id"])

        return users

    def get_user_by_id(self, user_id: str) -> User:
        user = self.repository.find_by_id(ObjectId(user_id))
        if user:
            user["_id"] = str(user["_id"])

        return user

    def create_user(self, payload: dict) -> str:
        return str(self.repository.create(CreateUserDTO(**payload).model_dump()))

    def update_user(self, user_id: str, payload: dict) -> bool:
        payload["updatedAt"] = datetime.now(timezone.utc)

        return self.repository.update(
            ObjectId(user_id), UpdateUserDTO(**payload).model_dump()
        )

    def delete_user(self, user_id: str) -> bool:
        return self.repository.delete(ObjectId(user_id))
