from fastapi import Depends
from pydantic import UUID4

from controllers.question_controller import QuestionController
from routers import APIRouter
from schemas.auth_schema import UserDetails
from schemas.question_schema import QuestionsSchema, QuestionResponse
from services.auth_service import get_current_active_user

router = APIRouter(prefix="/quizzes/{quiz_id}/questions", tags=["Questions"])


@router.get("/", response_model=list[QuestionResponse])
def get_questions(
    quiz_id: UUID4, current_user: UserDetails = Depends(get_current_active_user)
):
    """
    Get questions from quiz
    """
    return QuestionController.get_questions(quiz_id, current_user.id)


@router.post("/", status_code=204)
def add_questions(
    quiz_id: UUID4,
    question_data: QuestionsSchema,
    current_user: UserDetails = Depends(get_current_active_user),
):
    """
    Add questions to quiz
    """
    return QuestionController.add_questions(quiz_id, question_data, current_user.id)
