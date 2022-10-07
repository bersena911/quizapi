from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import sessionmaker

from controllers.question_controller import QuestionController
from controllers.quiz_controller import QuizController
from models.game_answer_model import GameAnswer
from models.game_model import Game
from models.game_question_model import GameQuestion
from schemas.game_answer_schema import GameAnswerSchema
from schemas.game_schema import GameStartSchema
from services.db_service import db_service


class GameController:
    @staticmethod
    def get_games(user_id: UUID4) -> dict:
        with sessionmaker(bind=db_service.engine)() as session:
            return session.query(Game).filter(Game.user_id == user_id).all()

    @staticmethod
    def start_game(game_body: GameStartSchema, user_id: UUID4):
        if not QuizController.check_quiz_exists(game_body.quiz_id):
            raise HTTPException(status_code=404, detail="Quiz not found")
        with sessionmaker(bind=db_service.engine)() as session:
            game = (
                session.query(Game)
                .filter(Game.quiz_id == game_body.quiz_id and Game.user_id == user_id)
                .first()
            )
            if not game:
                game = Game(
                    started=True,
                    finished=False,
                    score=0,
                    offset=0,
                    quiz_id=game_body.quiz_id,
                    user_id=user_id,
                )
                session.add(game)
                session.commit()
                return {"id": game.id}
            elif game.finished:
                raise HTTPException(
                    status_code=400, detail="You already played this game"
                )
            else:
                return {"id": game.id}

    @staticmethod
    def get_game(session, game_id: UUID4, user_id: UUID4) -> Game:
        game = (
            session.query(Game)
            .filter(Game.id == game_id and Game.user_id == user_id)
            .first()
        )
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        return game

    @staticmethod
    def get_game_question(session, game_id: UUID4, question_id: UUID4) -> GameQuestion:
        game_question = (
            session.query(GameQuestion)
            .filter(GameQuestion.id == question_id and GameQuestion.game_id == game_id)
            .first()
        )
        return game_question

    def next_question(self, game_id: UUID4, user_id: UUID4):
        with sessionmaker(bind=db_service.engine)() as session:
            game = self.get_game(session, game_id, user_id)
            if game.finished:
                raise HTTPException(status_code=400, detail="Game is already finished")
            question = QuestionController.paginate_questions(game.quiz_id, game.offset)
            if not question:
                game.finished = True
                session.commit()
                return

            game_question = (
                session.query(GameQuestion)
                .filter(GameQuestion.question_id == question.id and Game.id == game_id)
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
                "question_id": game_question.id,
                "question_type": question.type,
                "question": question.title,
                "answers": [
                    {"choice": answer.choice, "value": answer.value}
                    for answer in question.answers
                ],
            }

    @staticmethod
    def is_question_not_answered_or_skipped(game_question: GameQuestion) -> bool:
        if game_question.skipped:
            raise HTTPException(status_code=400, detail="Question already skipped")
        if game_question.answered:
            raise HTTPException(status_code=400, detail="Question already answered")
        return True

    def answer_question(
        self,
        answer_data: GameAnswerSchema,
        game_id: UUID4,
        question_id: UUID4,
        user_id: UUID4,
    ):
        with sessionmaker(bind=db_service.engine)() as session:
            game_question = self.get_game_question(session, game_id, question_id)
            if self.is_question_not_answered_or_skipped(game_question):
                game = self.get_game(session, game_question.game_id, user_id)
                game_question.answered = True
                for choice in answer_data.choices:
                    session.add(
                        GameAnswer(choice=choice, game_question_id=game_question.id)
                    )
                game.offset += 1
                session.commit()

    def skip_question(self, game_id: UUID4, question_id: UUID4, user_id: UUID4):
        with sessionmaker(bind=db_service.engine)() as session:
            game_question = self.get_game_question(session, game_id, question_id)
            if self.is_question_not_answered_or_skipped(game_question):
                game = self.get_game(session, game_question.game_id, user_id)
                game_question.skipped = True
                game.offset += 1
                session.commit()
