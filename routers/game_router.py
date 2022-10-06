from fastapi import Depends

from controllers.game_controller import GameController
from routers import APIRouter
from schemas.auth_schema import UserDetails
from schemas.game_schema import GameStartSchema
from services.auth_service import get_current_active_user

router = APIRouter(prefix="/games", tags=["Games"])


@router.post("/start")
def start_game(
    game_body: GameStartSchema,
    current_user: UserDetails = Depends(get_current_active_user),
):
    return GameController.start_game(game_body, current_user.id)
