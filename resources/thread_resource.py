from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from framework.database import get_db
from services.ThreadService import ThreadService
from models.thread import ThreadCreate, ThreadRead

router = APIRouter(prefix="/threads", tags=["Threads"])
thread_service = ThreadService()

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from framework.database import get_db
from models.thread import ThreadCreate, ThreadRead
from services.ThreadService import ThreadService

router = APIRouter(prefix="/threads", tags=["Threads"])
thread_service = ThreadService()


@router.post("/", response_model=ThreadRead, status_code=status.HTTP_201_CREATED)
def create_thread(thread_data: ThreadCreate, db: Session = Depends(get_db)):
    new_thread = thread_service.create_thread(db, thread_data)
    return ThreadRead.model_validate(new_thread)

