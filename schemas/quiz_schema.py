from pydantic import BaseModel, UUID4


class QuizSchema(BaseModel):
    title: str

    class Config:
        """Extra configuration options"""

        anystr_strip_whitespace = True
        min_anystr_length = 1


class QuizCreateResponse(BaseModel):
    id: UUID4


class QuizResponse(BaseModel):
    id: UUID4
    title: str
    published: bool
