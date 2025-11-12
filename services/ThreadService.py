from sqlalchemy.orm import Session
from models.orm_thread import Thread
from models.thread import ThreadCreate 
from uuid import uuid4
from datetime import datetime

class ThreadService:
    def create_thread(self, db: Session, thread_data: ThreadCreate):
        """Create a new thread and save it to the database."""
        new_thread = Thread(
            author_id=str(thread_data.author_id), 
            thread_type=thread_data.thread_type,
            title=thread_data.title,
            content=thread_data.content or "",
            is_active=thread_data.is_active,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_thread)
        db.commit()
        db.refresh(new_thread)
        return new_thread

    def get_thread(self, db: Session, thread_id):
        return db.query(Thread).filter(Thread.id == thread_id).first()
