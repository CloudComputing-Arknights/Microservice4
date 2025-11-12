from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4


class MessageBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4, 
        description="Unique ID for the message."
    )
    sender_id: UUID = Field(
        description="UUID of the user who sent this message."
    )
    content: str = Field(
        min_length=1, 
        description="Content of the message."
    )
    time_stamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Time when the message was sent (UTC)."
    )

    class Config:
        orm_mode = True


class MessageCreate(BaseModel):
    sender_id: UUID = Field(description="UUID of the message sender.")
    content: str = Field(min_length=1, max_length=1000, description="Message text content.")

    class Config:
        json_schema_extra = {
            "example": {
                "sender_id": "123e4567-e89b-12d3-a456-426614174000",
                "content": "Hi, is this item still available?"
            }
        }


class MessageUpdate(BaseModel):
    content: Optional[str] = Field(None, description="Updated message content.")

    class Config:
        json_schema_extra = {
            "example": {"content": "Hey, I changed my mind — can we meet tomorrow?"}
        }


class MessageRead(MessageBase):
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Message creation timestamp (UTC).")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp (UTC).")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "sender_id": "123e4567-e89b-12d3-a456-426614174000",
                "content": "Got it, thank you!",
                "time_stamp": "2025-11-10T12:34:56Z",
                "created_at": "2025-11-10T12:34:56Z",
                "updated_at": "2025-11-10T12:45:00Z"
            }
        }
    }
