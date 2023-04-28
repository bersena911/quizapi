from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from controllers.question_controller import QuestionController
from helpers.pagination_helper import Paginate
from routers import APIRouter
from schemas.auth_schema import UserDetails
from schemas.question_schema import (
    QuestionsSchema,
    QuestionResponse,
    UpdateQuestionSchema,
)
from services.auth_service import get_current_active_user
from services.db_service import get_session

router = APIRouter(prefix="/quizzes/{quiz_id}/questions", tags=["Questions"])


@router.get("/", response_model=Paginate[QuestionResponse])
def get_questions(
    quiz_id: UUID4,
    current_user: UserDetails = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """
    Get questions from quiz
    """
    return QuestionController.get_questions(session, quiz_id, current_user.id)


@router.post("/", status_code=204)
def add_questions(
    quiz_id: UUID4,
    question_data: QuestionsSchema,
    current_user: UserDetails = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """
    Add questions to quiz
    """
    return QuestionController().add_questions(
        session, quiz_id, question_data, current_user.id
    )


@router.delete("/{question_id}", status_code=204)
def delete_question(
    quiz_id: UUID4,
    question_id: UUID4,
    current_user: UserDetails = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """
    Delete question from quiz
    """
    return QuestionController().delete_question(
        session, quiz_id, question_id, current_user.id
    )


@router.patch("/{question_id}", status_code=204)
def update_question(
    quiz_id: UUID4,
    question_id: UUID4,
    question_data: UpdateQuestionSchema,
    current_user: UserDetails = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """
    Update question in quiz
    """
    return QuestionController().update_question(
        session, quiz_id, question_id, question_data, current_user.id
    )
