from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import sessionmaker

from controllers.quiz_controller import QuizController
from models.answer_model import Answer
from models.question_model import Question
from schemas.question_schema import (
    QuestionsSchema,
    QuestionTypeEnum,
    UpdateQuestionSchema,
)
from services.db_service import db_service


class QuestionController:
    @staticmethod
    def get_questions(quiz_id: UUID4, user_id: UUID4) -> dict:
        """
        Retrieves questions from quiz
        Args:
            quiz_id: quiz id
            user_id: authenticated user id

        Returns:

        """
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = QuizController.get_quiz_for_user(session, quiz_id, user_id)
            items = [
                {
                    "id": question.id,
                    "title": question.title,
                    "type": question.type,
                    "answers": [answer.__dict__ for answer in question.answers],
                }
                for question in session.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            ]
            return {
                "total_count": len(items),
                "limit": len(items),
                "offset": 0,
                "items": items,
            }

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
    def validate_answers(answers: list, question_type: QuestionTypeEnum):
        correct_answers = 0
        for answer in answers:
            if answer.is_correct:
                correct_answers += 1
        if question_type == QuestionTypeEnum.SINGLE_ANSWER and correct_answers > 1:
            raise HTTPException(
                status_code=400,
                detail=f"{question_type.value} can't have multiple correct answers",
            )
        if correct_answers == 0:
            raise HTTPException(
                status_code=400,
                detail="There must be at least one correct answer",
            )

    def add_questions(
        self, quiz_id: UUID4, questions_data: QuestionsSchema, user_id: UUID4
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
                self.validate_answers(question_data.answers, question_data.type)
                question = Question(
                    title=question_data.title,
                    type=question_data.type.value,
                    quiz_id=quiz.id,
                    answers=[
                        Answer(value=answer.value, is_correct=answer.is_correct)
                        for answer in question_data.answers
                    ],
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

    def delete_question(
        self, quiz_id: UUID4, question_id: UUID4, user_id: UUID4
    ) -> None:
        """
        Deletes question from quiz if quiz is not published
        Args:
            quiz_id: quiz id
            question_id: question id
            user_id: authenticated user id

        Returns:

        """
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = QuizController.get_quiz_for_user(session, quiz_id, user_id)
            if quiz.published:
                raise HTTPException(
                    status_code=400, detail="Can't delete question from published quiz"
                )
            question = self.get_question(session, question_id)
            session.delete(question)
            session.commit()

    def update_question(
        self,
        quiz_id: UUID4,
        question_id: UUID4,
        question_data: UpdateQuestionSchema,
        user_id: UUID4,
    ) -> None:
        """
        Deletes question from quiz if quiz is not published
        Args:
            quiz_id: quiz id
            question_id: question id
            question_data: Question Data
            user_id: authenticated user id

        Returns:

        """
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = QuizController.get_quiz_for_user(session, quiz_id, user_id)
            if quiz.published:
                raise HTTPException(
                    status_code=400, detail="Can't update question from published quiz"
                )
            question = self.get_question(session, question_id)
            if question_data.type and question_data.answers:
                self.validate_answers(question_data.answers, question_data.type)
                question.answers = [
                    Answer(value=answer.value, is_correct=answer.is_correct)
                    for answer in question_data.answers
                ]
                question.type = question_data.type.value
            elif question_data.type and question_data.type != question.type:
                self.validate_answers(question.answers, question_data.type)
                question.type = question_data.type.value
            elif question_data.answers:
                self.validate_answers(
                    question_data.answers, QuestionTypeEnum[question.type]
                )
                question.answers = [
                    Answer(value=answer.value, is_correct=answer.is_correct)
                    for answer in question_data.answers
                ]
            if question_data.title:
                question.title = question_data.title
            session.commit()
