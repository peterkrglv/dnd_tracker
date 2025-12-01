from uuid import UUID

from fastapi import HTTPException, status
from pydantic import EmailStr

from app.db.models.user import User
from app.db.repos.user_repository import UserRepository
from app.utils.security import (
    create_access_token,
    get_password_hash,
    get_user_id_from_token,
    verify_password,
)


class UserService:
    def __init__(self):
        self.user_repo = None

    def set_repository(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def signup(
        self, email: str, password: str, username: str | None = None
    ) -> str:
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_password = get_password_hash(password)
        user = await self.user_repo.create(email, hashed_password, username)
        return create_access_token(data={"sub": str(user.id)})

    async def login_user(self, email: EmailStr, password: str) -> str:
        user = await self.user_repo.get_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        return create_access_token(data={"sub": str(user.id)})

    async def get_current_user(self, token: str) -> User:
        user_id = get_user_id_from_token(token)
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user

    async def update_user(
        self,
        user_id: UUID,
        email: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ) -> User:
        if not self.user_repo:
            raise RuntimeError("Repository not set")

        update_data = {}
        if email is not None:
            update_data["email"] = email
        if username is not None:
            update_data["username"] = username
        if password is not None:
            update_data["password"] = get_password_hash(password)

        user = await self.user_repo.update_user(user_id, update_data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return user
