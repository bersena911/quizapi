from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from models.game_model import Game
from models.game_question_model import GameQuestion
from models.question_model import Question
from models.quiz_model import Quiz
from models.user_model import User
from schemas.quiz_schema import QuizSchema, UpdateQuizSchema


class QuizController:
    @staticmethod
    def create_quiz(session: Session, quiz_data: QuizSchema, user_id: UUID4) -> dict:
        """
        Creates empty quiz
        Args:
            session: db session
            quiz_data: quiz data
            user_id: authenticated user id

        Returns:
            dict: containing quiz id

        """
        quiz = Quiz(title=quiz_data.title, published=False, user_id=user_id)
        session.add(quiz)
        session.commit()
        return {"id": quiz.id}

    @staticmethod
    def get_quiz(session: Session, quiz_id: UUID4) -> Quiz:
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
    def get_quiz_for_user(session: Session, quiz_id: UUID4, user_id: UUID4) -> Quiz:
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

    def get_quiz_details(
        self, session: Session, quiz_id: UUID4, user_id: UUID4
    ) -> Quiz:
        """
        Retrieves quiz created by user
        Args:
            session: db session
            quiz_id: quiz id
            user_id: authenticated user id

        Returns:
            sqlalchemy Quiz object

        """
        return self.get_quiz_for_user(session, quiz_id, user_id)

    @staticmethod
    def get_quizzes(session: Session, user_id: UUID4, limit: int, offset: int) -> dict:
        """
        Retrieves quizzes created by user
        Args:
            session: db session
            user_id: authenticated user id
            limit: limit
            offset: offset

        Returns:
            list of Quiz objects

        """
        query = (
            session.query(Quiz.id, Quiz.title, Quiz.published, Quiz.created_at)
            .filter(Quiz.user_id == user_id)
            .filter(Quiz.deleted.is_(False))
        )
        quizzes = query.limit(limit).offset(offset).all()
        return {
            "total_count": query.count(),
            "limit": limit,
            "offset": offset,
            "items": quizzes,
        }

    def publish_quiz(self, session: Session, quiz_id: UUID4, user_id: UUID4) -> None:
        """
        Updates quiz row as published in db
        Args:
            quiz_id: quiz id
            user_id: authenticated user id

        Returns:

        """
        quiz = self.get_quiz_for_user(session, quiz_id, user_id)
        if len(quiz.questions) == 0:
            raise HTTPException(
                status_code=400, detail="Can't publish quiz without questions"
            )
        quiz.published = True
        session.commit()

    def delete_quiz(self, session: Session, quiz_id: UUID4, user_id: UUID4) -> None:
        """
        Updates quiz row as deleted in db
        Args:
            session: db session
            quiz_id: quiz id
            user_id: authenticated user id

        Returns:

        """
        quiz = self.get_quiz_for_user(session, quiz_id, user_id)
        quiz.deleted = True
        session.commit()

    def update_quiz(
        self,
        session: Session,
        quiz_id: UUID4,
        quiz_data: UpdateQuizSchema,
        user_id: UUID4,
    ) -> None:
        """
        Updates quiz row as deleted in db
        Args:
            session: db session
            quiz_id: quiz id
            quiz_data: quiz data
            user_id: authenticated user id

        Returns:

        """
        quiz = self.get_quiz_for_user(session, quiz_id, user_id)
        if quiz.published:
            raise HTTPException(status_code=400, detail="Can't update published quiz")
        quiz.title = quiz_data.title
        session.commit()

    def get_quiz_games(
        self, session: Session, quiz_id: UUID4, user_id: UUID4, limit: int, offset: int
    ) -> dict:
        """
        Retrieves games played in the quiz
        Args:
            session: db session
            quiz_id: quiz id
            user_id: authenticated user id
            limit: limit
            offset: offset

        Returns:
            list of games played in the quiz

        """
        quiz = self.get_quiz_for_user(session, quiz_id, user_id)
        query = (
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
        )
        games = query.limit(limit).offset(offset).all()
        return {
            "total_count": query.count(),
            "limit": limit,
            "offset": offset,
            "items": games,
        }

    def get_quiz_game_details(
        self, session: Session, quiz_id: UUID4, game_id: UUID4, user_id: UUID4
    ):
        """
        Retrieves detailed info about quiz game
        Args:
            session: db session
            quiz_id: quiz id
            game_id: game id
            user_id: authenticated user id

        Returns:
            stats about single question

        """
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
