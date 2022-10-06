import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from services.db_service import Base


class GameAnswer(Base):
    __tablename__ = "users_answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    choice = Column(String)
    users_question_id = Column(UUID(as_uuid=True), ForeignKey("users_questions.id"))
