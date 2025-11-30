import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from framework.database import get_db
from models.message import MessageCreate, MessageRead
from services.MessagingService import MessageService
from typing import List
from uuid import UUID

logger = logging.getLogger("messaging-ms.message-resource")
router = APIRouter(prefix="/threads", tags=["Messaging"])
message_service = MessageService()


@router.post("/{thread_id}/messages", response_model=MessageRead, status_code=status.HTTP_201_CREATED)
async def send_message(
    thread_id: UUID,
    message_data: MessageCreate,
    db: AsyncSession = Depends(get_db)
):
    logger.info(
        f"Sending message in thread={thread_id} "
        f"from sender={message_data.sender_id}"
    )

    try:
        message = await message_service.create_message(
            db=db,
            thread_id=str(thread_id),
            sender_id=str(message_data.sender_id),
            content=message_data.content
        )

        logger.info(
            f"Message created successfully: id={message.id}, thread={thread_id}"
        )

        return MessageRead.model_validate(message)

    except Exception as e:
        logger.error(
            f"Failed to send message in thread={thread_id}: {e}"
        )
        raise HTTPException(status_code=500, detail="Failed to send message")


@router.get("/{thread_id}/messages", response_model=List[MessageRead])
async def get_messages(
    thread_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Fetching messages for thread={thread_id}")

    try:
        messages = await message_service.get_messages_by_thread(db, str(thread_id))

        logger.info(
            f"Found {len(messages)} messages for thread={thread_id}"
        )

        return [MessageRead.model_validate(msg) for msg in messages]

    except Exception as e:
        logger.error(
            f"Failed to fetch messages for thread={thread_id}: {e}"
        )
        raise HTTPException(status_code=500, detail="Failed to fetch messages")
