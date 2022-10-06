from fastapi import Depends

from controllers.question_controller import QuestionController
from routers import APIRouter
from schemas.auth_schema import UserDetails
from schemas.question_schema import QuestionsSchema
from services.auth_service import get_current_active_user

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/", status_code=204)
def add_questions(
    question_data: QuestionsSchema,
    current_user: UserDetails = Depends(get_current_active_user),
):
    """
    Add questions to quiz
    """
    return QuestionController.add_questions(question_data, current_user.id)
