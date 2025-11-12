from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4


class ThreadBase(BaseModel):
    """Common fields shared by all thread schemas."""
    author_id: UUID = Field(description="The user who created the thread.")
    thread_type: str = Field(description="Type of thread (e.g. item_discussion, general_chat).")
    item_id: Optional[UUID] = Field(None, description="Related item UUID, if applicable.")
    title: str = Field(min_length=3, max_length=100, description="Title of the discussion thread.")
    content: Optional[str] = Field(None, description="Optional initial message or thread description.")
    is_active: bool = Field(True, description="Whether the thread is open for discussion.")


class ThreadCreate(ThreadBase):
    """Schema used when creating a new thread."""
    class Config:
        json_schema_extra = {
            "example": {
                "author_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "thread_type": "item_discussion",
                "item_id": "i1i2i3i4-i5i6-i7i8-i9i0-i1i2i3i4i5i6",
                "title": "Discussion about the IKEA Sofa",
                "content": "I saw this sofa listed and had a few questions about its condition.",
                "is_active": True
            }
        }


class ThreadUpdate(BaseModel):
    """Partial update schema."""
    title: Optional[str] = Field(None, description="Updated title for the thread.")
    content: Optional[str] = Field(None, description="Updated content for the thread.")
    is_active: Optional[bool] = Field(None, description="Set thread active/inactive.")


class ThreadRead(ThreadBase):
    """Returned to the client when fetching thread info."""
    thread_id: UUID = Field(..., alias="id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "from_attributes": True,      
        "populate_by_name": True, 
        "json_schema_extra": {
            "example": {
                "thread_id": "550e8400-e29b-41d4-a716-446655440000",
                "author_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                "thread_type": "item_discussion",
                "item_id": "i1i2i3i4-i5i6-i7i8-i9i0-i1i2i3i4i5i6",
                "title": "Discussion about the IKEA Sofa",
                "content": "I saw this sofa listed and had a few questions about its condition.",
                "is_active": True,
                "created_at": "2025-11-10T12:34:56Z",
                "updated_at": "2025-11-10T12:45:00Z"
            }
        }
    }
