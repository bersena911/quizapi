from fastapi import Depends
from pydantic import UUID4

from controllers.quiz_controller import QuizController
from routers import APIRouter
from schemas.auth_schema import UserDetails
from schemas.quiz_schema import (
    QuizSchema,
    QuizCreateResponse,
    QuizDetails,
)
from services.auth_service import get_current_active_user

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])


@router.post("/", response_model=QuizCreateResponse)
def create_quiz(
    quiz_data: QuizSchema, current_user: UserDetails = Depends(get_current_active_user)
):
    """
    Create empty quiz
    """
    return QuizCreateResponse(**QuizController.create_quiz(quiz_data, current_user.id))


@router.get("/")
def get_user_quizzes(current_user: UserDetails = Depends(get_current_active_user)):
    """
    Create empty quiz
    """
    return QuizController.get_quizzes(current_user.id)


@router.get("/{quiz_id}", response_model=QuizDetails)
def get_quiz_details(
    quiz_id: UUID4, current_user: UserDetails = Depends(get_current_active_user)
):
    return QuizDetails(**QuizController.get_quiz_details(quiz_id, current_user.id))
