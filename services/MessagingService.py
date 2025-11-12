from models.orm_message import Message
from models.orm_thread import Thread
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from uuid import UUID, uuid4



class MessageService:
    def create_message(self, db, thread_id, sender_id, content):
        thread = db.query(Thread).filter(Thread.id == str(thread_id)).first()

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
            created_at=datetime.utcnow(),
        )

        db.add(new_message)
        db.commit()
        db.refresh(new_message)
        return new_message

    @staticmethod
    def get_messages_by_thread(db: Session, thread_id: UUID):
        return (
            db.query(Message)
            .filter_by(thread_id=str(thread_id))
            .order_by(Message.created_at.asc())
            .all()
        )

