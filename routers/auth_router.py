from fastapi import Depends

from controllers.auth_controller import AuthController
from routers import APIRouter
from schemas.auth_schema import (
    RegisterSchema,
    LoginSchema,
    UserDetails,
    RegisterResponse,
    LoginResponse,
)
from services.auth_service import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=RegisterResponse)
def register(register_data: RegisterSchema):
    """
    User Registration endpoint
    """
    return RegisterResponse(**AuthController().register(register_data))


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginSchema):
    """
    User Login endpoint
    """
    return LoginResponse(**AuthController().login(login_data))


@router.get("/me", response_model=UserDetails)
def me(current_user: UserDetails = Depends(get_current_user)):
    """
    Returns authenticated users details
    """
    return current_user
