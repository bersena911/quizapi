from pydantic import BaseModel, UUID4


class AnswerSchema(BaseModel):
    value: str
    is_correct: bool

    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True
        min_anystr_length = 1


class AnswerResponse(BaseModel):
    id: UUID4
    value: str
    is_correct: bool
