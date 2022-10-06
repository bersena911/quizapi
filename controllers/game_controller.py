from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import sessionmaker

from controllers.quiz_controller import QuizController
from models.game_model import Game
from schemas.game_schema import GameStartSchema
from services.db_service import db_service


class GameController:
    @staticmethod
    def start_game(game_body: GameStartSchema, user_id: UUID4):
        if not QuizController.check_quiz_exists(game_body.quiz_id):
            raise HTTPException(status_code=404, detail="Quiz not found")
        with sessionmaker(bind=db_service.engine)() as session:
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
