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

    @staticmethod
    def next_question(game_id: UUID4, user_id: UUID4):
        with sessionmaker(bind=db_service.engine)() as session:
            game = (
                session.query(Game)
                .filter(Game.id == game_id and Game.user_id == user_id)
                .first()
            )
            if not game:
                raise HTTPException(status_code=404, detail="Game not found")
            question = QuestionController.paginate_questions(game.quiz_id, game.offset)
            if not question:
                return
            game.offset += 1

            game_question = GameQuestion(answered=False, skipped=False, game_id=game_id)
            session.add(game_question)
            session.commit()
            return {
                "question_id": game_question.id,
                "question": question.title,
                "answers": [
                    {"choice": answer.choice, "value": answer.value}
                    for answer in question.answers
                ],
            }

    @staticmethod
    def answer_question(
        game_id: UUID4, question_id: UUID4, answer_data: GameAnswerSchema
    ):
        with sessionmaker(bind=db_service.engine)() as session:
            game_question = (
                session.query(GameQuestion)
                .filter(GameQuestion.id == question_id and Game.id == game_id)
                .first()
            )
            game_question.answered = True
            for choice in answer_data.choices:
                session.add(
                    GameAnswer(choice=choice, game_question_id=game_question.id)
                )
            session.commit()
