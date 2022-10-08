from pydantic import BaseModel, UUID4


class GameStartSchema(BaseModel):
    quiz_id: UUID4


class StartGameResponse(BaseModel):
    id: UUID4


class GameResponse(BaseModel):
    id: UUID4
    quiz_id: UUID4
    title: str
    finished: bool
    score: float


class QuestionStat(BaseModel):
    answer_score: float
    title: str


class FinalResultsResponse(BaseModel):
    score: float
    score_percentage: float
    question_stats: list[QuestionStat]
