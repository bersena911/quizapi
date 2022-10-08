from pydantic import BaseModel, UUID4


class AnswerSchema(BaseModel):
    value: str
    is_correct: bool


class AnswerResponse(BaseModel):
    id: UUID4
    value: str
    is_correct: bool
