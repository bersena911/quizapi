from controllers.auth_controller import AuthController
from routers import APIRouter
from schemas.auth_schema import RegisterSchema, LoginSchema

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(register_data: RegisterSchema):
    """
    User Registration endpoint
    """
    return AuthController().register(register_data)


@router.post("/login")
def login(login_data: LoginSchema):
    """
    User Login endpoint
    """
    return AuthController().login(login_data)
