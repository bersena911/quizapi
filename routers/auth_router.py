from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from controllers.auth_controller import AuthController
from routers import APIRouter
from schemas.auth_schema import (
    RegisterSchema,
    LoginSchema,
    UserDetails,
    RegisterResponse,
    LoginResponse,
)
from services.auth_service import get_current_user, authorization_header_scheme

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=RegisterResponse)
def register(register_data: RegisterSchema):
    """
    User Registration endpoint
    """
    return AuthController().register(register_data)


@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginSchema):
    """
    User Login endpoint
    """
    return AuthController().login(login_data)


@router.post("/refresh", response_model=LoginResponse)
def refresh(token: HTTPAuthorizationCredentials = Depends(authorization_header_scheme)):
    """
    User Login endpoint
    """
    return AuthController().refresh_token(token.credentials)


@router.get("/me", response_model=UserDetails)
def me(current_user: UserDetails = Depends(get_current_user)):
    """
    Returns authenticated users details
    """
    return current_user
