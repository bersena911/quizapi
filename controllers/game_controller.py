from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import update
from sqlalchemy.orm import sessionmaker

from controllers.question_controller import QuestionController
from controllers.quiz_controller import QuizController
from models.answer_model import Answer
from models.game_answer_model import GameAnswer
from models.game_model import Game
from models.game_question_model import GameQuestion
from models.question_model import Question
from models.quiz_model import Quiz
from schemas.game_answer_schema import GameAnswerSchema
from schemas.game_schema import GameStartSchema
from schemas.question_schema import QuestionTypeEnum
from services.db_service import db_service


class GameController:
    @staticmethod
    def get_games(user_id: UUID4) -> list:
        """
        Lists all games for user
        Args:
            user_id: user_id for filtering

        Returns:
            list: games played by user

        """
        with sessionmaker(bind=db_service.engine)() as session:
            return (
                session.query(
                    Quiz.title, Game.id, Game.finished, Game.score, Game.quiz_id
                )
                .join(Quiz.games)
                .filter(Game.user_id == user_id)
                .all()
            )

    @staticmethod
    def start_game(game_body: GameStartSchema, user_id: UUID4) -> dict:
        """
        Creates empty game with default values
        Args:
            game_body: payload containing quiz_id
            user_id: authenticated user id

        Returns:
            id of started game

        """
        with sessionmaker(bind=db_service.engine)() as session:
            quiz = QuizController.get_quiz(session, game_body.quiz_id)
            if quiz.deleted or not quiz.published:
                raise HTTPException(status_code=404, detail="Quiz not found")
            game = (
                session.query(Game)
                .filter(Game.quiz_id == game_body.quiz_id)
                .filter(Game.user_id == user_id)
                .first()
            )
            if not game:
                game = Game(
                    finished=False,
                    score=0,
                    offset=0,
                    quiz_id=game_body.quiz_id,
                    user_id=user_id,
                )
                session.add(game)
                session.commit()
                return {"id": game.id}
            if game.finished:
                raise HTTPException(
                    status_code=400, detail="You already played this game"
                )
            return {"id": game.id}

    @staticmethod
    def get_game(session, game_id: UUID4, user_id: UUID4) -> Game:
        """
        Retrieves game by game id
        Args:
            session: sqlalchemy session
            game_id: game id
            user_id: authenticated user id

        Returns:
            sqlalchemy Game object

        """
        game = (
            session.query(*Quiz.__table__.columns, *Game.__table__.columns)
            .join(Quiz.games)
            .filter(Game.id == game_id)
            .filter(Game.user_id == user_id)
            .first()
        )
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        return game

    @staticmethod
    def get_game_question(session, game_id: UUID4, question_id: UUID4) -> GameQuestion:
        """
        Retrieves info about answered question
        Args:
            session: sqlalchemy session
            game_id: game id
            question_id: question id

        Returns:
            sqlalchemy GameQuestion object

        """
        game_question = (
            session.query(GameQuestion)
            .filter(GameQuestion.id == question_id)
            .filter(GameQuestion.game_id == game_id)
            .first()
        )
        return game_question

    def next_question(self, game_id: UUID4, user_id: UUID4) -> dict:
        """
        Retrieves next question to answer from quiz, if not answered or skipped always returns same
        Args:
            game_id: game id
            user_id: authenticated user id

        Returns:
            questions details if there is next questions, otherwise raises error

        """
        with sessionmaker(bind=db_service.engine)() as session:
            game = self.get_game(session, game_id, user_id)
            if game.finished:
                raise HTTPException(status_code=400, detail="Game is already finished")
            question = QuestionController.paginate_questions(game.quiz_id, game.offset)
            if not question:
                session.execute(
                    update(Game).where(Game.id == game.id).values(finished=True)
                )
                session.commit()
                raise HTTPException(status_code=400, detail="Game is already finished")

            game_question = (
                session.query(GameQuestion)
                .filter(GameQuestion.question_id == question.id)
                .filter(GameQuestion.game_id == game_id)
                .first()
            )
            if not game_question:
                game_question = GameQuestion(
                    answered=False,
                    skipped=False,
                    game_id=game_id,
                    question_id=question.id,
                )
                session.add(game_question)
                session.commit()
            return {
                "id": game_question.id,
                "type": question.type,
                "title": question.title,
                "answers": [answer.__dict__ for answer in question.answers],
            }

    @staticmethod
    def check_question_answered_or_skipped(game_question: GameQuestion) -> None:
        """
        Raises exceptions if question is already skipped or answered
        Args:
            game_question: game question object

        Returns:

        """
        if game_question.skipped:
            raise HTTPException(status_code=400, detail="Question already skipped")
        if game_question.answered:
            raise HTTPException(status_code=400, detail="Question already answered")

    @staticmethod
    def calculate_answer_score(
        user_choices: list[UUID4], actual_answers: list[Answer], question_type: str
    ) -> float:
        """
        Calculates score for current answered question
        Args:
            user_choices: choices user made
            actual_answers: actual answers stored in db
            question_type: type of question

        Returns:
            float: score

        """
        correct_answers_set = set()
        false_answers_set = set()

        for actual_answer in actual_answers:
            if actual_answer.is_correct:
                correct_answers_set.add(actual_answer.id)
            else:
                false_answers_set.add(actual_answer.id)

        if question_type == QuestionTypeEnum.SINGLE_ANSWER.value:
            if user_choices[0] in correct_answers_set:
                return 1
            if user_choices[0] in false_answers_set:
                return -1
            raise HTTPException(status_code=400, detail="Choice not in choices list")

        if question_type == QuestionTypeEnum.MULTIPLE_ANSWERS.value:
            plus_score = 0
            minus_score = 0
            for user_choice in user_choices:
                if user_choice in correct_answers_set:
                    plus_score += 1
                elif user_choice in false_answers_set:
                    minus_score += 1
                else:
                    raise HTTPException(
                        status_code=400, detail="Choice not in choices list"
                    )

            plus_score = plus_score / len(correct_answers_set)
            minus_score = minus_score / len(false_answers_set)

            return plus_score - minus_score

        raise ValueError("Unknown question_type")

    def answer_question(
        self,
        answer_data: GameAnswerSchema,
        game_id: UUID4,
        question_id: UUID4,
        user_id: UUID4,
    ) -> None:
        """
        Saves info about answered question
        Args:
            answer_data: user sent data
            game_id: game id
            question_id: question id
            user_id: authenticated user id

        Returns:

        """
        with sessionmaker(bind=db_service.engine)() as session:
            game = self.get_game(session, game_id, user_id)
            game_question = self.get_game_question(session, game_id, question_id)
            self.check_question_answered_or_skipped(game_question)
            question = QuestionController.get_question(
                session, game_question.question_id
            )
            if question.type == QuestionTypeEnum.SINGLE_ANSWER.value:
                if len(answer_data.choices) > 1:
                    raise HTTPException(
                        status_code=400,
                        detail=f"{question.type} does not support multiple answers",
                    )
            score = self.calculate_answer_score(
                answer_data.choices, question.answers, question.type
            )
            session.execute(
                update(Game)
                .where(Game.id == game.id)
                .values(score=game.score + score, offset=game.offset + 1)
            )
            game_question.answer_score = score
            game_question.answered = True
            for choice in answer_data.choices:
                session.add(
                    GameAnswer(choice=choice, game_question_id=game_question.id)
                )
            session.commit()

    def skip_question(self, game_id: UUID4, question_id: UUID4, user_id: UUID4) -> None:
        """
        Skips question without modifying anything
        Args:
            game_id: game id
            question_id: question id
            user_id: authenticated user id

        Returns:

        """
        with sessionmaker(bind=db_service.engine)() as session:
            game = self.get_game(session, game_id, user_id)
            game_question = self.get_game_question(session, game_id, question_id)
            self.check_question_answered_or_skipped(game_question)
            game_question.answer_score = 0
            game_question.skipped = True
            session.execute(
                update(Game).where(Game.id == game.id).values(offset=game.offset + 1)
            )
            session.commit()

    def get_results(self, game_id: UUID4, user_id: UUID4) -> dict:
        """
        Retrieves final results of the finished game
        Args:
            game_id: game id
            user_id: authenticated user id

        Returns:

        """
        with sessionmaker(bind=db_service.engine)() as session:
            game = self.get_game(session, game_id, user_id)
            if not game.finished:
                raise HTTPException(status_code=400, detail="Game is not finished yet")
            question_stats = (
                session.query(GameQuestion.answer_score, Question.title)
                .join(Question, Question.id == GameQuestion.question_id)
                .filter(GameQuestion.game_id == game_id)
                .all()
            )
            max_score = len(question_stats)
            score_percentage = game.score / max_score * 100
            return {
                "score": game.score,
                "score_percentage": score_percentage,
                "question_stats": question_stats,
            }
