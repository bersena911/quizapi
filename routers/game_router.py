from fastapi import Depends
from pydantic import UUID4

from controllers.game_controller import GameController
from routers import APIRouter
from schemas.auth_schema import UserDetails
from schemas.game_answer_schema import GameAnswerSchema
from schemas.game_schema import GameStartSchema
from services.auth_service import get_current_active_user

router = APIRouter(prefix="/games", tags=["Games"])


@router.post("/start")
def start_game(
    game_body: GameStartSchema,
    current_user: UserDetails = Depends(get_current_active_user),
):
    return GameController.start_game(game_body, current_user.id)


@router.post("/{game_id}/questions/next")
def next_question(
    game_id: UUID4,
    current_user: UserDetails = Depends(get_current_active_user),
):
    return GameController.next_question(game_id, current_user.id)


@router.post("/{game_id}/questions/{question_id}/submit")
def answer_question(
    game_id: UUID4,
    question_id: UUID4,
    answer_data: GameAnswerSchema,
):
    return GameController.answer_question(game_id, question_id, answer_data)


@router.get("/{game_id}/questions/results")
def get_results():
    pass
