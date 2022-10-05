from pydantic import BaseModel, EmailStr


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