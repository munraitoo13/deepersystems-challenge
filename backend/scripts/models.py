from dataclasses import dataclass
from datetime import datetime


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
    updatedAt: datetime | None = None
    active: bool
