import uuid

from sqlalchemy import Column, String, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from services.db_service import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(Integer, autoincrement=True)
    title = Column(String)
    type = Column(Boolean)
    quiz_id = Column(UUID, ForeignKey("quizzes.id"))
    answers = relationship("Answer")
