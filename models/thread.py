from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4


class ThreadBase(BaseModel):
    """Common fields shared by all thread schemas."""
    author_id: UUID = Field(description="The user who created the thread.")
    participant_id: UUID = Field(description="The other person in the conversation.")


class ThreadCreate(BaseModel):
    author_id: UUID = Field(description="User starting the conversation.")
    participant_id: UUID = Field(description="Other user in the DM thread.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "author_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "participant_id": "bb12cc34-dd56-ee78-9900-aabbccddeeff"
            }
        }
    }


class ThreadUpdate(BaseModel):
    """Partial update schema."""


class ThreadRead(ThreadBase):
    """Returned to the client when fetching thread info."""
    thread_id: UUID
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "thread_id": "550e8400-e29b-41d4-a716-446655440000",
                "author_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "participant_id": "bb12cc34-dd56-ee78-9900-aabbccddeeff",
                "created_at": "2025-11-10T12:34:56Z",
                "updated_at": "2025-11-10T12:35:56Z"
            }
        }
    }
