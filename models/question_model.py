import uuid

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from services.db_service import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String)
    type = Column(String)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    answers = relationship("Answer", lazy=False)
