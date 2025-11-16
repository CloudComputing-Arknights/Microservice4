from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone
import uuid
from framework.database import Base
from models.orm_message import relationship

class Thread(Base):
    __tablename__ = "thread"

    thread_id = Column(String(36), primary_key=True)

    author_id = Column(String(36), nullable=False)
    participant_id = Column(String(36), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    messages = relationship("Message", back_populates="thread")

