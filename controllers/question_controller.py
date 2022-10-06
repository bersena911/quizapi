from pydantic import UUID4
from sqlalchemy.orm import sessionmaker

from controllers.quiz_controller import QuizController
from models.answer_model import Answer
from models.question_model import Question
from schemas.question_schema import QuestionsSchema
from services.db_service import db_service


class QuestionController:
    @staticmethod
    def add_questions(questions_data: QuestionsSchema, user_id: UUID4) -> None:
        quiz = QuizController.get_quiz_details(questions_data.quiz_id, user_id)
        with sessionmaker(bind=db_service.engine)() as session:
            for question_data in questions_data.questions:
                answers = []
                for answer in question_data.answers:
                    answers.append(
                        Answer(choice=answer.choice, is_correct=answer.is_correct)
                    )
                question = Question(
                    title=question_data.title,
                    type=question_data.type.value,
                    quiz_id=questions_data.quiz_id,
                    answers=answers,
                )
                session.add(question)
            session.commit()
