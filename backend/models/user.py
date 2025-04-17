from dataclasses import dataclass
from datetime import datetime
from backend.models.user_preferences import UserPreferences


@dataclass
class User:
    username: str
    password: str
    roles: list[str]
    preferences: UserPreferences
    createdAt: float = datetime.now()
    updatedAt: float | None = None
    active: bool = True
