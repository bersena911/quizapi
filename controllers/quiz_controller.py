from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import sessionmaker

from models.quiz_model import Quiz
from schemas.quiz_schema import QuizSchema
from services.db_service import db_service


class QuizController:
    @staticmethod
    def create_quiz(quiz_data: QuizSchema, user_id: UUID4) -> dict:
        """
        Creates empty quiz
        Args:
            quiz_data: quiz data
            user_id: authenticated user id

        Returns:
            dict: containing quiz id

        """
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = Quiz(title=quiz_data.title, published=False, user_id=user_id)
            session.add(quiz)
            session.commit()
            return {"id": quiz.id}

    @staticmethod
    def get_quiz(session, quiz_id: UUID4) -> Quiz:
        quiz = (
            session.query(Quiz)
            .filter((Quiz.id == quiz_id) & (Quiz.deleted.is_(False)))
            .first()
        )
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        return quiz

    @staticmethod
    def get_quiz_for_user(session, quiz_id: UUID4, user_id: UUID4) -> Quiz:
        quiz = (
            session.query(Quiz)
            .filter(
                (Quiz.id == quiz_id)
                & (Quiz.user_id == user_id)
                & (Quiz.deleted.is_(False))
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
