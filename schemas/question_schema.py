from enum import Enum

from pydantic import BaseModel, UUID4

from schemas.answers_schema import AnswerSchema


class QuestionTypeEnum(Enum):
    SINGLE_ANSWER = "SINGLE_ANSWER"
    MULTIPLE_ANSWERS = "MULTIPLE_ANSWERS"


class QuestionSchema(BaseModel):
    title: str
    type: QuestionTypeEnum
    answers: list[AnswerSchema]

    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True
        min_anystr_length = 1


class QuestionsSchema(BaseModel):
    quiz_id: UUID4
    questions: list[QuestionSchema]
