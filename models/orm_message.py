from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from framework.database import Base


class Message(Base):
    """
    Represents a message in a conversation thread between two users.
    Each message belongs to a specific thread and is sent by one user.
    """

    __tablename__ = "message"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    thread_id = Column(String(36), ForeignKey("thread.thread_id"), nullable=False)
    sender_id = Column(String(36), nullable=False)
    content = Column(String(1000), nullable=False)
    time_stamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    thread = relationship("Thread", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, sender_id={self.sender_id}, thread_id={self.thread_id})>"
