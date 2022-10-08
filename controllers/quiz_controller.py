from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import sessionmaker

from models.game_model import Game
from models.game_question_model import GameQuestion
from models.question_model import Question
from models.quiz_model import Quiz
from models.user_model import User
from schemas.quiz_schema import QuizSchema, UpdateQuizSchema
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
        """
        Retrieves quiz by id
        Args:
            session: sqlalchemy session
            quiz_id: quiz id

        Returns:
            sqlalchemy Quiz object

        """
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
        """
        Retrieves quiz created by user
        Args:
            session: sqlalchemy session
            quiz_id: quiz id
            user_id: authenticated user id

        Returns:
            sqlalchemy Quiz object

        """
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

    def get_quiz_details(self, quiz_id: UUID4, user_id: UUID4) -> Quiz:
        """
        Retrieves quiz created by user
        Args:
            quiz_id: quiz id
            user_id: authenticated user id

        Returns:
            sqlalchemy Quiz object

        """
        with sessionmaker(bind=db_service.engine)() as session:
            return self.get_quiz_for_user(session, quiz_id, user_id)

    @staticmethod
    def get_quizzes(user_id: UUID4) -> list[Quiz]:
        """
        Retrieves quizzes created by user
        Args:
            user_id: authenticated user id

        Returns:
            list of Quiz objects

        """
        with sessionmaker(bind=db_service.engine)() as session:
            return (
                session.query(Quiz.id, Quiz.title, Quiz.published)
                .filter(Quiz.user_id == user_id)
                .filter(Quiz.deleted.is_(False))
                .all()
            )

    def publish_quiz(self, quiz_id: UUID4, user_id: UUID4) -> None:
        """
        Updates quiz row as published in db
        Args:
            quiz_id: quiz id
            user_id: authenticated user id

        Returns:

        """
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = self.get_quiz_for_user(session, quiz_id, user_id)
            quiz.published = True
            session.commit()

    def delete_quiz(self, quiz_id: UUID4, user_id: UUID4) -> None:
        """
        Updates quiz row as deleted in db
        Args:
            quiz_id: quiz id
            user_id: authenticated user id

        Returns:

        """
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = self.get_quiz_for_user(session, quiz_id, user_id)
            quiz.deleted = True
            session.commit()

    def update_quiz(
        self, quiz_id: UUID4, quiz_data: UpdateQuizSchema, user_id: UUID4
    ) -> None:
        """
        Updates quiz row as deleted in db
        Args:
            quiz_id: quiz id
            quiz_data: quiz data
            user_id: authenticated user id

        Returns:

        """
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = self.get_quiz_for_user(session, quiz_id, user_id)
            if quiz.published:
                raise HTTPException(
                    status_code=400, detail="Can't update published quiz"
                )
            quiz.title = quiz_data.title
            session.commit()

    def get_quiz_games(self, quiz_id: UUID4, user_id: UUID4):
        """
        Retrieves games played in the quiz
        Args:
            quiz_id: quiz id
            user_id: authenticated user id

        Returns:
            list of games played in the quiz

        """
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = self.get_quiz_for_user(session, quiz_id, user_id)
            return (
                session.query(
                    Game.id,
                    Game.finished,
                    Game.score,
                    Game.quiz_id,
                    Game.user_id,
                    Quiz.title,
                    User.username,
                )
                .join(Quiz, Game.quiz_id == Quiz.id)
                .join(User, Game.user_id == User.id)
                .filter(Game.quiz_id == quiz.id)
                .all()
            )

    def get_quiz_game_details(self, quiz_id: UUID4, game_id: UUID4, user_id: UUID4):
        """
        Retrieves detailed info about quiz game
        Args:
            quiz_id: quiz id
            game_id: game id
            user_id: authenticated user id

        Returns:
            stats about single question

        """
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = self.get_quiz_for_user(session, quiz_id, user_id)
            question_stats = (
                session.query(GameQuestion.answer_score, Question.title)
                .join(Question, Question.id == GameQuestion.question_id)
                .filter(GameQuestion.game_id == game_id)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )
            return {
                "question_stats": question_stats,
            }
