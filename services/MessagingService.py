from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from models.orm_thread import Thread
from models.orm_message import Message
from datetime import datetime
from uuid import uuid4


class MessageService:

    async def create_message(self, db, thread_id, sender_id, content):
        result = await db.execute(
            select(Thread).where(Thread.thread_id == thread_id)
        )
        thread = result.scalar_one_or_none()

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

        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)
        return new_message

    async def get_messages_by_thread(self, db, thread_id):
        result = await db.execute(
            select(Message)
            .where(Message.thread_id == thread_id)
            .order_by(Message.time_stamp.asc())
        )
        return result.scalars().all()
