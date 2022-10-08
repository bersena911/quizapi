import uuid

from sqlalchemy import Column, ForeignKey, Boolean, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from services.db_service import Base


class GameQuestion(Base):
    __tablename__ = "game_questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    answered = Column(Boolean)
    skipped = Column(Boolean)
    answer_score = Column(Float)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), index=True)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"))
    game_answers = relationship("GameAnswer", lazy=False)
