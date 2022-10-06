from pydantic import BaseModel


class GameAnswerSchema(BaseModel):
    choices: list
