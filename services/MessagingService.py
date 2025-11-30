import logging
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from models.orm_thread import Thread
from models.orm_message import Message
from datetime import datetime
from uuid import uuid4

logger = logging.getLogger("messaging-ms.service.message")

class MessageService:
    async def create_message(self, db, thread_id, sender_id, content):
        logger.info(f"Attempting to create message in thread={thread_id} from sender={sender_id}")
        try:
            result = await db.execute(
                select(Thread).where(Thread.thread_id == thread_id)
            )
            thread = result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"DB error while checking thread existence: {e}")
            raise HTTPException(status_code=500, detail="Database error")
        
        if not thread:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Thread not found"
            )

        new_message = Message(
            id=str(uuid4()),
            thread_id=str(thread_id),
            sender_id=str(sender_id),
            content=content,
            time_stamp=datetime.utcnow(),
        )

        try:
            db.add(new_message)
            await db.commit()
            await db.refresh(new_message)

            logger.info(
                f"Message created successfully: id={new_message.id}, thread={thread_id}"
            )

            return new_message

        except Exception as e:
            logger.error(f"Failed to create message in thread={thread_id}: {e}")
            await db.rollback()
            raise HTTPException(status_code=500, detail="Failed to create message")

    async def get_messages_by_thread(self, db, thread_id):
        logger.info(f"Fetching messages for thread={thread_id}")
        try:
            result = await db.execute(
                select(Message)
                .where(Message.thread_id == thread_id)
                .order_by(Message.time_stamp.asc())
            )
            messages = result.scalars().all()

            logger.info(f"Retrieved {len(messages)} messages for thread={thread_id}")

            return messages

        except Exception as e:
            logger.error(f"Failed to fetch messages for thread={thread_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to fetch messages"
            )