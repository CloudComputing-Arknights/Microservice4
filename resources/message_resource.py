from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from framework.database import get_db
from models.message import MessageCreate, MessageRead
from services.MessagingService import MessageService
from typing import List
from uuid import UUID

router = APIRouter(prefix="/threads", tags=["Messaging"])

message_service = MessageService()


@router.post("/{thread_id}/messages", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
def send_message(
    thread_id: UUID,
    message_data: MessageCreate,
    db: Session = Depends(get_db)
):
    """Create a new message within a thread."""
    message = message_service.create_message(
        db=db,
        thread_id=thread_id,
        sender_id=message_data.sender_id,
        content=message_data.content
    )
    return MessageRead.from_orm(message)


@router.get("/{thread_id}/messages", response_model=List[MessageRead])
def get_messages(thread_id: UUID, db: Session = Depends(get_db)):
    """Retrieve all messages in a specific thread."""
    messages = message_service.get_messages_by_thread(db, thread_id)
    return [MessageRead.from_orm(m) for m in messages]
