from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from framework.database import Base


class Thread(Base):
    __tablename__ = "thread"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    author_id = Column(String(36), nullable=False)
    thread_type = Column(String(50), nullable=False)
    title = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="thread", cascade="all, delete-orphan")
