from backend.scripts.models import User, UserPreferences
from datetime import datetime, timezone


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
