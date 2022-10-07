from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import sessionmaker

from models.quiz_model import Quiz
from schemas.quiz_schema import QuizSchema
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
    def check_quiz_published(session, quiz_id: UUID4) -> bool:
        return (
            session.query(Quiz)
            .filter(
                Quiz.id == quiz_id
                and Quiz.deleted.is_(False)
                and Quiz.published.is_(True)
            )
            .exists()
        ).scalar()

    @staticmethod
    def get_quiz_for_user(session, quiz_id: UUID4, user_id: UUID4):
        quiz = (
            session.query(Quiz)
            .filter(
                Quiz.id == quiz_id
                and Quiz.user_id == user_id
                and Quiz.deleted.is_(False)
            )
            .first()
        )
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        return quiz

    def get_quiz_details(self, quiz_id: UUID4, user_id: UUID4) -> dict:
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = self.get_quiz_for_user(session, quiz_id, user_id)
            quiz_details = quiz.__dict__
            return quiz_details

    @staticmethod
    def get_quizzes(user_id: UUID4) -> dict:
        with sessionmaker(bind=db_service.engine)() as session:
            return (
                session.query(Quiz)
                .filter(Quiz.user_id == user_id)
                .filter(Quiz.deleted.is_(False))
                .all()
            )

    def publish_quiz(self, quiz_id: UUID4, user_id: UUID4):
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = self.get_quiz_for_user(session, quiz_id, user_id)
            quiz.published = True
            session.commit()

    def delete_quiz(self, quiz_id: UUID4, user_id: UUID4):
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = self.get_quiz_for_user(session, quiz_id, user_id)
            quiz.deleted = True
            session.commit()
