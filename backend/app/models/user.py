from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserPreferences:
    timezone: str


@dataclass
class User:
    username: str
    password: str
    roles: list[str]
    preferences: UserPreferences
    createdAt: datetime
    updatedAt: datetime
    active: bool
