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
