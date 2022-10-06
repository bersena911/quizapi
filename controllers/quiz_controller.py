from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import sessionmaker

from models.quiz_model import Quiz
from schemas.quiz_schema import QuizSchema, QuizDetails
from services.db_service import db_service


class QuizController:
    @staticmethod
    def create_quiz(quiz_data: QuizSchema, user_id: UUID4) -> dict:
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = Quiz(title=quiz_data.title, published=False, user_id=user_id)
            session.add(quiz)
            session.commit()
            return {"id": quiz.id}

    @staticmethod
    def get_quiz_details(quiz_id: UUID4, user_id: UUID4) -> dict:
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = (
                session.query(Quiz)
                .filter(Quiz.id == quiz_id and Quiz.user_id == user_id)
                .first()
            )
            if not quiz:
                raise HTTPException(status_code=404, detail="Quiz not found")
            quiz_details = QuizDetails(**quiz.__dict__).dict()
            return quiz_details
