import uuid

from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID

from services.db_service import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    choice = Column(String)
    value = Column(String)
    is_correct = Column(Boolean)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"))
