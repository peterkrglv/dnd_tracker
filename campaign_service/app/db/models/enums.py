import enum

from sqlalchemy import Enum as SAEnum


class UserStatus(str, enum.Enum):
    MASTER = "master"
    PLAYER = "player"


user_status_enum = SAEnum(
    UserStatus,
    name="user_status",
    create_constraint=True,
    validate_strings=True,
)
