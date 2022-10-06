from pydantic import BaseModel, UUID4


class AnswerSchema(BaseModel):
    choice: str
    is_correct: bool
