from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import sessionmaker

from controllers.quiz_controller import QuizController
from models.users_quiz_model import UsersQuiz
from services.db_service import db_service


class UsersQuizController:
    @staticmethod
    def start_quiz(quiz_id: UUID4, user_id: UUID4):
        if not QuizController.check_quiz_exists(quiz_id):
            raise HTTPException(status_code=404, detail="Quiz not found")
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = UsersQuiz(
                started=True,
                finished=False,
                score=0,
                offset=0,
                quiz_id=quiz_id,
                user_id=user_id,
            )
            session.add(quiz)
            session.commit()
            return {"id": quiz.id}
