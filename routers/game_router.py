from fastapi import Depends
from pydantic import UUID4

from controllers.game_controller import GameController
from routers import APIRouter
from schemas.auth_schema import UserDetails
from schemas.game_answer_schema import GameAnswerSchema
from schemas.game_schema import GameStartSchema
from services.auth_service import get_current_active_user

router = APIRouter(prefix="/games", tags=["Games"])


@router.get("/")
def get_user_games(current_user: UserDetails = Depends(get_current_active_user)):
    return GameController.get_games(current_user.id)


@router.post("/start")
def start_game(
    game_body: GameStartSchema,
    current_user: UserDetails = Depends(get_current_active_user),
):
    """
    Start a new game from quiz
    """
    return GameController.start_game(game_body, current_user.id)


@router.get("/{game_id}/questions/next")
def next_question(
    game_id: UUID4,
    current_user: UserDetails = Depends(get_current_active_user),
):
    """
    Retrieves next question, returns same if question is not answered or skipped.
    """
    return GameController().next_question(game_id, current_user.id)


@router.post("/{game_id}/questions/{question_id}/submit", status_code=204)
def answer_question(
    game_id: UUID4,
    question_id: UUID4,
    answer_data: GameAnswerSchema,
    current_user: UserDetails = Depends(get_current_active_user),
):
    """
    Answer a question
    """
    return GameController().answer_question(
        answer_data, game_id, question_id, current_user.id
    )


@router.post("/{game_id}/questions/{question_id}/skip", status_code=204)
def skip_question(
    game_id: UUID4,
    question_id: UUID4,
    current_user: UserDetails = Depends(get_current_active_user),
):
    """
    Skip question
    """
    return GameController().skip_question(game_id, question_id, current_user.id)


@router.get("/{game_id}/results")
def get_results(
    game_id: UUID4,
    current_user: UserDetails = Depends(get_current_active_user),
):
    """
    Get final results
    """
    return GameController().get_results(game_id, current_user.id)
