from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

authorization_header_scheme = HTTPBearer(auto_error=False)


def decode_token(token: str):
    # TODO REAL TOKEN DECODER HERE
    return {"user_id": "1"}


async def auth_required_dependency(
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(authorization_header_scheme),
):
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
    user_details = decode_token(token.credentials)
    request.state.user_details = user_details
    return user_details
