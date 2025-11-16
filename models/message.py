from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4


class MessageBase(BaseModel):
    sender_id: UUID = Field(description="UUID of the sender")
    content: str = Field(min_length=1, description="Content of the message.")
    time_stamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Time when the message was sent (UTC).")
    model_config = {"from_attributes": True}


class MessageCreate(BaseModel):
    sender_id: UUID
    content: str = Field(min_length=1, max_length=1000)

    model_config = {
        "json_schema_extra": {
            "example": {
                "sender_id": "123e4567-e89b-12d3-a456-426614174000",
                "content": "Hey! Are you still selling the mirror?"
            }
        }
    }


class MessageUpdate(BaseModel):
    content: Optional[str] = Field(None, description="Updated message content.")

    model_config = {
        "json_schema_extra": {
            "example": {"content": "Updated message text"}
        }
    }


class MessageRead(MessageBase):
    id: UUID = Field(default_factory=uuid4)
    thread_id: UUID = Field(description="Thread this message belongs to")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "thread_id": "123e4567-e89b-12d3-a456-426614173000",
                "sender_id": "123e4567-e89b-12d3-a456-426614174000",
                "content": "Got it, thank you!",
                "time_stamp": "2025-11-10T12:34:56Z",
                "created_at": "2025-11-10T12:34:56Z",
                "updated_at": "2025-11-10T12:45:00Z"
            }
        }
    }
