from pydantic import BaseModel, EmailStr, UUID4


class RegisterSchema(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True
        min_anystr_length = 1


class LoginSchema(BaseModel):
    username: str
    password: str

    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True
        min_anystr_length = 1


class RegisterResponse(BaseModel):
    user_id: UUID4


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class UserDetails(BaseModel):
    id: UUID4
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    disabled: bool
