import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.orm_thread import Thread
from models.thread import ThreadCreate 
from uuid import uuid4
from datetime import datetime

logger = logging.getLogger("messaging-ms.service.thread")
class ThreadService:
    async def create_thread(self, db: AsyncSession, thread_data: ThreadCreate):
        """Create a new thread and save it to the database."""
        logger.info(f"Creating new thread between author={thread_data.author_id} and participant={thread_data.participant_id}")
        new_thread = Thread(
            thread_id=str(uuid4()),
            author_id=str(thread_data.author_id),
            participant_id=str(thread_data.participant_id),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        try:
            db.add(new_thread)
            await db.commit()
            await db.refresh(new_thread)

            logger.info(
                f"Thread created successfully: id={new_thread.thread_id}"
            )

            return new_thread

        except Exception as e:
            logger.error(f"Failed to create thread: {e}")
            await db.rollback()
            raise

    async def get_thread(self, db: AsyncSession, thread_id: str):
        logger.info(f"Fetching thread with id={thread_id}")
        
        try:
            result = await db.execute(
                select(Thread).where(Thread.thread_id == thread_id)
            )

            thread = result.scalar_one_or_none()

            if thread is None:
                logger.warning(f"Thread not found: id={thread_id}")
            else:
                logger.info(f"Thread retrieved: id={thread_id}")
            return thread

        except Exception as e:
            logger.error(f"Error fetching thread id={thread_id}: {e}")
            raise
