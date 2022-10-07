from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import sessionmaker

from controllers.quiz_controller import QuizController
from models.answer_model import Answer
from models.question_model import Question
from schemas.question_schema import QuestionsSchema
from services.db_service import db_service


class QuestionController:
    @staticmethod
    def get_questions(quiz_id: UUID4):
        with sessionmaker(bind=db_service.engine)() as session:
            return session.query(Question).filter(Question.quiz_id == quiz_id).all()

    @staticmethod
    def add_questions(
        quiz_id: UUID4, questions_data: QuestionsSchema, user_id: UUID4
    ) -> None:
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = QuizController.get_quiz_for_user(quiz_id, user_id)
            if not quiz:
                raise HTTPException(status_code=404, detail="Quiz not found")
            for question_data in questions_data.questions:
                answers = []
                for answer in question_data.answers:
                    answers.append(
                        Answer(
                            choice=answer.choice,
                            value=answer.value,
                            is_correct=answer.is_correct,
                        )
                    )
                question = Question(
                    title=question_data.title,
                    type=question_data.type.value,
                    quiz_id=quiz_id,
                    answers=answers,
                )
                session.add(question)
            session.commit()

    @staticmethod
    def paginate_questions(quiz_id: UUID4, offset: int) -> Question:
        with sessionmaker(bind=db_service.engine)() as session:
            return (
                session.query(Question)
                .filter(Question.quiz_id == quiz_id)
                .limit(1)
                .offset(offset)
                .first()
            )
