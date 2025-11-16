from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from framework.database import get_db
from models.message import MessageCreate, MessageRead
from services.MessagingService import MessageService
from typing import List
from uuid import UUID

router = APIRouter(prefix="/threads", tags=["Messaging"])
message_service = MessageService()


@router.post("/{thread_id}/messages", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
async def send_message(
    thread_id: UUID,
    message_data: MessageCreate,
    db: AsyncSession = Depends(get_db)
):
    message = await message_service.create_message(
        db=db,
        thread_id=str(thread_id),
        sender_id=str(message_data.sender_id),
        content=message_data.content
    )

    return MessageRead.model_validate(message)


@router.get("/{thread_id}/messages", response_model=List[MessageRead])
async def get_messages(
    thread_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    messages = await message_service.get_messages_by_thread(db, str(thread_id))
    return [MessageRead.model_validate(msg) for msg in messages]
