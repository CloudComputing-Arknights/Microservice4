from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.orm_thread import Thread
from models.thread import ThreadCreate 
from uuid import uuid4
from datetime import datetime

class ThreadService:
    async def create_thread(self, db: AsyncSession, thread_data: ThreadCreate):
        """Create a new thread and save it to the database."""
        new_thread = Thread(
            thread_id=str(uuid4()),
            author_id=str(thread_data.author_id),
            participant_id=str(thread_data.participant_id),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(new_thread)
        await db.commit()
        await db.refresh(new_thread)
        return new_thread

    async def get_thread(self, db: AsyncSession, thread_id: str):
        result = await db.execute(
            select(Thread).where(Thread.thread_id == thread_id)
        )
        return result.scalar_one_or_none()
