from fastapi import APIRouter, Depends

from app.config.dependencies import get_current_user, get_user_service
from app.db.models.user import User
from app.schemas.user_schemas import (
    TokenResponse,
    UserLogin,
    UserResponse,
    UserSignup,
    UserUpdate,
)
from app.user_service import UserService

router = APIRouter(tags=["user"])


@router.post("/signup", response_model=TokenResponse)
async def signup(
    user_data: UserSignup, user_service: UserService = Depends(get_user_service)
):
    access_token = await user_service.signup(
        user_data.email, user_data.password, user_data.username
    )
    return TokenResponse(access_token=access_token)


@router.post("/login", response_model=TokenResponse)
async def login(
    user_data: UserLogin, user_service: UserService = Depends(get_user_service)
):
    access_token = await user_service.login_user(user_data.email, user_data.password)
    return TokenResponse(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    user = await user_service.update_user(current_user, user_data)
    return UserResponse.model_validate(user)
