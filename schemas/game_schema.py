from pydantic import BaseModel, UUID4


class GameStartSchema(BaseModel):
    quiz_id: UUID4
