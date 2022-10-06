import uuid

from sqlalchemy import Column, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from services.db_service import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    started = Column(Boolean)
    finished = Column(Boolean)
    score = Column(Integer)
    offset = Column(Integer)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    quiz_id = Column(UUID(as_uuid=True), ForeignKey("quizzes.id"))
    game_questions = relationship("GameQuestion")
