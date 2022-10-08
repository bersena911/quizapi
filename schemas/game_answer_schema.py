from pydantic import BaseModel, UUID4


class GameAnswerSchema(BaseModel):
    choices: list[UUID4]
