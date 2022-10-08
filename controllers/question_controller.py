from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import sessionmaker

from controllers.quiz_controller import QuizController
from models.answer_model import Answer
from models.question_model import Question
from schemas.question_schema import QuestionsSchema, QuestionTypeEnum
from services.db_service import db_service


class QuestionController:
    @staticmethod
    def get_questions(quiz_id: UUID4, user_id: UUID4) -> list[Question]:
        """
        Retrieves questions from quiz
        Args:
            quiz_id: quiz id
            user_id: authenticated user id

        Returns:

        """
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = QuizController.get_quiz_for_user(session, quiz_id, user_id)
            return session.query(Question).filter(Question.quiz_id == quiz.id).all()

    @staticmethod
    def get_question(session, question_id: UUID4) -> Question:
        """
        Retrieves detailed info about question
        Args:
            session: sqlalchemy session
            question_id: question id

        Returns:
            sqlalchemy Question object

        """
        question = session.query(Question).filter(Question.id == question_id).first()
        if not question:
            raise HTTPException(status_code=400, detail="Question not found")
        return question

    @staticmethod
    def add_questions(
        quiz_id: UUID4, questions_data: QuestionsSchema, user_id: UUID4
    ) -> None:
        """
        Adds questions to already created unpublished quiz
        Args:
            quiz_id: quiz id
            questions_data: questions data
            user_id: authenticated user id

        Returns:

        """
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = QuizController.get_quiz_for_user(session, quiz_id, user_id)
            if quiz.published:
                raise HTTPException(
                    status_code=400,
                    detail="Can't add questions to already published quiz",
                )
            if len(questions_data.questions) + len(quiz.questions) > 10:
                raise HTTPException(
                    status_code=400,
                    detail="Maximum number of questions per quiz is 10",
                )
            for question_data in questions_data.questions:
                answers = []
                correct_answers = 0
                for answer in question_data.answers:
                    if answer.is_correct:
                        correct_answers += 1
                    answers.append(
                        Answer(
                            value=answer.value,
                            is_correct=answer.is_correct,
                        )
                    )
                if (
                    question_data.type == QuestionTypeEnum.SINGLE_ANSWER
                    and correct_answers > 1
                ):
                    raise HTTPException(
                        status_code=400,
                        detail=f"{question_data.type.value} can't have multiple correct answers",
                    )
                if correct_answers == 0:
                    raise HTTPException(
                        status_code=400,
                        detail="There must be at least one correct answer",
                    )
                question = Question(
                    title=question_data.title,
                    type=question_data.type.value,
                    quiz_id=quiz.id,
                    answers=answers,
                )
                session.add(question)
            session.commit()

    @staticmethod
    def paginate_questions(quiz_id: UUID4, offset: int) -> Question:
        """
        Retrieves questions one by one
        Args:
            quiz_id: quiz id
            offset: current progress in game

        Returns:
            sqlalchemy Questions object

        """
        with sessionmaker(bind=db_service.engine)() as session:
            return (
                session.query(Question)
                .filter(Question.quiz_id == quiz_id)
                .limit(1)
                .offset(offset)
                .first()
            )
