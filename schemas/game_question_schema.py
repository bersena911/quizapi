from pydantic import BaseModel, UUID4

from schemas.question_schema import QuestionTypeEnum


class NextQuestionAnswersResponse(BaseModel):
    id: UUID4
    value: str


class NextQuestionResponse(BaseModel):
    id: UUID4
    type: QuestionTypeEnum
    title: str
    answers: list[NextQuestionAnswersResponse]
