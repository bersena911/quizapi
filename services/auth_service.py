from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from schemas.auth_schema import UserDetails
from settings import app_config

ALGORITHM = "HS256"
SECRET_KEY = app_config["SECRET_KEY"]

authorization_header_scheme = HTTPBearer(auto_error=False)


def decode_token(token: str) -> dict:
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_token


async def get_current_user(
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(authorization_header_scheme),
) -> UserDetails:
    """
    Checks auth token and returns user details
    Args:
        request: Fast API Request object
        token: bearer token for auth

    Returns:
        details of authenticated user
    """
    if not token:
        raise HTTPException(status_code=401, detail="Authorization Header Not Provided")
    decoded_token = decode_token(token.credentials)

    user_details = UserDetails(**decoded_token)
    request.state.user_details = user_details
    return user_details


async def get_current_active_user(
    current_user: UserDetails = Depends(get_current_user),
) -> UserDetails:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
