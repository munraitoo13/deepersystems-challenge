from datetime import datetime, timezone
from pydantic import BaseModel, Field


class UserPreferencesDTO(BaseModel):
    timezone: str


class CreateUserDTO(BaseModel):
    username: str
    password: str
    roles: list[str]
    preferences: UserPreferencesDTO
    createdAt: datetime = datetime.now(timezone.utc)
    updatedAt: datetime | None = None
    active: bool = True


class UpdateUserDTO(BaseModel):
    username: str
    password: str
    roles: list[str]
    preferences: UserPreferencesDTO
    updatedAt: datetime
    active: bool
