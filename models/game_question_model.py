import uuid

from sqlalchemy import Column, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from services.db_service import Base


class GameQuestion(Base):
    __tablename__ = "users_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    answered = Column(Boolean)
    skipped = Column(Boolean)
    users_quiz_id = Column(UUID(as_uuid=True), ForeignKey("users_quizzes.id"))
    answers = relationship("GameAnswer")
