from fastapi import Depends
from pydantic import UUID4

from controllers.quiz_controller import QuizController
from routers import APIRouter
from schemas.auth_schema import UserDetails
from schemas.quiz_schema import (
    QuizSchema,
    QuizCreateResponse,
    QuizResponse,
    UpdateQuizSchema,
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


@router.get("/", response_model=list[QuizResponse])
def get_user_quizzes(current_user: UserDetails = Depends(get_current_active_user)):
    """
    Create empty quiz
    """
    return QuizController.get_quizzes(current_user.id)


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz_details(
    quiz_id: UUID4, current_user: UserDetails = Depends(get_current_active_user)
):
    """
    Retrieve Quiz Details
    """
    return QuizController().get_quiz_details(quiz_id, current_user.id).__dict__


@router.patch("/{quiz_id}/publish", status_code=204)
def publish_quiz(
    quiz_id: UUID4, current_user: UserDetails = Depends(get_current_active_user)
):
    """
    Publish quiz
    """
    return QuizController().publish_quiz(quiz_id, current_user.id)


@router.delete("/{quiz_id}", status_code=204)
def delete_quiz(
    quiz_id: UUID4, current_user: UserDetails = Depends(get_current_active_user)
):
    """
    Delete quiz
    """
    return QuizController().delete_quiz(quiz_id, current_user.id)


@router.patch("/{quiz_id}", status_code=204)
def update_quiz(
    quiz_id: UUID4,
    quiz_data: UpdateQuizSchema,
    current_user: UserDetails = Depends(get_current_active_user),
):
    """
    Update quiz
    """
    return QuizController().update_quiz(quiz_id, quiz_data, current_user.id)
