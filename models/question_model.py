import uuid

from sqlalchemy import Column, String, ForeignKey, Integer, Sequence
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from services.db_service import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(Integer, Sequence("questions_order_id_seq"))
    title = Column(String)
    type = Column(String)
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    answers = relationship("Answer", lazy=True)
