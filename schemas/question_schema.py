from enum import Enum

from pydantic import BaseModel, conlist

from schemas.answers_schema import AnswerSchema


class QuestionTypeEnum(Enum):
    SINGLE_ANSWER = "SINGLE_ANSWER"
    MULTIPLE_ANSWERS = "MULTIPLE_ANSWERS"


class QuestionSchema(BaseModel):
    title: str
    type: QuestionTypeEnum
    answers: conlist(AnswerSchema, min_items=2, max_items=5)

    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True
        min_anystr_length = 1


class QuestionsSchema(BaseModel):
    questions: conlist(QuestionSchema, min_items=1, max_items=10)
