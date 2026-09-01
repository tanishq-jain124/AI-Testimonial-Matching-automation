from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from app.db import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False)
    email_id = Column(String(320), unique=True, nullable=False, index=True)
    social_id = Column(String(1000), nullable=True)
    batch = Column(String(100), nullable=True)
    pass_hash = Column(String(255), nullable=False)

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    user_1_from = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    user_2_to = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    message = Column(Text, nullable=False)

class Testimonial(Base):
    __tablename__ = "testimonials"
    testimonial_id = Column(Integer, primary_key=True)
    author_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    target_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False, index=True)
    testimonial_text = Column(Text, nullable=False)
    similarity_score = Column(String(50), nullable=True)
    generation_attempt = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    __table_args__ = (
        UniqueConstraint("author_user_id", "target_user_id", name="uq_testimonial_author_target"),
    )
