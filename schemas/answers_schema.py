from pydantic import BaseModel


class AnswerSchema(BaseModel):
    choice: str
    value: str
    is_correct: bool
