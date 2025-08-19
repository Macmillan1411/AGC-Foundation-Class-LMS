from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    url = Column(String, unique=True, index=True, nullable=False)
    published = Column(Integer, default=0)  # 0 for not published, 1 for published
    order = Column(Integer, default=0)  # Order for sorting videos
    quizzes = relationship("QuizQuestion", back_populates="video", cascade="all, delete-orphan")
