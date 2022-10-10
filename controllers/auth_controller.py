from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from models.user_model import User
from schemas.auth_schema import RegisterSchema, LoginSchema, UserDetails
from services.db_service import db_service
from settings import app_config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
SECRET_KEY = app_config["SECRET_KEY"]


class AuthController:
    @staticmethod
    def create_access_token(
        data: dict, expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
    ) -> str:
        """
        Creates access token using python-jose library
        Args:
            data: data to encode inside token
            expire_minutes: optional token expiration time. defaults to 30

        Returns:
            str: created access token

        """
        to_encode = data.copy()
        to_encode["id"] = str(to_encode["id"])
        expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def refresh_token(
        self, token: str, expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
    ) -> dict:
        """
        Creates access token using python-jose library
        Args:
            token: current token
            expire_minutes: optional token expiration time. defaults to 30

        Returns:
            str: created access token

        """
        to_encode = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False}
        )
        access_token = self.create_access_token(to_encode)
        return {"access_token": access_token, "token_type": "Bearer"}

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies password using passlib library
        Args:
            plain_password: raw password from input
            hashed_password: hashed password from db

        Returns:
            bool: True if password matches otherwise False

        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Creates hash from password using passlib library
        Args:
            password: raw password from input

        Returns:
            str: hashed password

        """
        return pwd_context.hash(password)

    def check_user_access(self, user: User, password: str):
        """
        Checks if found user matches given password
        Args:
            user: user from db
            password: password from input

        Returns:
            bool: True if user matches, otherwise False

        """
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return True

    @staticmethod
    def check_user_exists(session, username: str, email: str) -> bool:
        """
        checks if user already exists in db
        Args:
            session: session of sqlalchemy
            username: username
            email: email

        Returns:

        """
        if session.query(exists().where(User.email == email)).scalar():
            raise HTTPException(status_code=401, detail="Email already taken")
        if session.query(exists().where(User.username == username)).scalar():
            raise HTTPException(status_code=401, detail="Username already taken")
        return True

    def register(self, register_data: RegisterSchema) -> dict:
        """
        Registers user in db from input data
        Args:
            register_data: registration data containing user info

        Returns:
            str: registered user_id

        """
        with sessionmaker(bind=db_service.engine)() as session:
            self.check_user_exists(session, register_data.username, register_data.email)
            user = User(
                username=register_data.username,
                first_name=register_data.first_name,
                last_name=register_data.last_name,
                email=register_data.email,
                password=self.get_password_hash(register_data.password),
                disabled=False,
            )
            session.add(user)
            session.commit()
            return {"user_id": user.id}

    def login(self, login_data: LoginSchema) -> dict:
        """
        Authenticates user with password and username
        Args:
            login_data: LoginSchema containing username and password

        Returns:
            dict: containing access_token and token_type

        """

        with sessionmaker(bind=db_service.engine)() as session:
            user = (
                session.query(User).filter(User.username == login_data.username).first()
            )

        if not self.check_user_access(user, login_data.password):
            raise HTTPException(
                status_code=401, detail="Incorrect username or password"
            )
        user_details = UserDetails(**user.__dict__).dict()
        access_token = self.create_access_token(
            data={"sub": user.username, **user_details}
        )
        return {"access_token": access_token, "token_type": "Bearer"}
