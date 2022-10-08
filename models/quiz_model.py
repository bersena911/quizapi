import uuid

from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from services.db_service import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    published = Column(Boolean)
    deleted = Column(Boolean, index=True, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    questions = relationship("Question")
    games = relationship("Game")
