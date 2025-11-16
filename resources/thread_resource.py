from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from framework.database import get_db
from services.ThreadService import ThreadService
from models.thread import ThreadCreate, ThreadRead

router = APIRouter(prefix="/threads", tags=["Threads"])
thread_service = ThreadService()

@router.post("/", response_model=ThreadRead, status_code=status.HTTP_201_CREATED)
async def create_thread(
    thread_data: ThreadCreate,
    db: AsyncSession = Depends(get_db)
):
    new_thread = await thread_service.create_thread(db, thread_data)
    return ThreadRead.model_validate(new_thread)

@router.get("/{thread_id}", response_model=ThreadRead)
async def get_thread(thread_id: str, db: AsyncSession = Depends(get_db)):
    thread = await thread_service.get_thread(db, thread_id)

    if thread is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thread not found")

    return ThreadRead.model_validate(thread)