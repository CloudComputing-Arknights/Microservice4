import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from framework.database import get_db
from services.ThreadService import ThreadService
from models.thread import ThreadCreate, ThreadRead

logger = logging.getLogger("messaging-ms.thread-resource")
router = APIRouter(prefix="/threads", tags=["Threads"])
thread_service = ThreadService()

@router.post("/", response_model=ThreadRead, status_code=status.HTTP_201_CREATED)
async def create_thread(thread_data: ThreadCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Creating thread with title='{thread_data.title}'")
    try:
        new_thread = await thread_service.create_thread(db, thread_data)
        logger.info(f"Thread created successfully: id={new_thread.id}")

        return ThreadRead.model_validate(new_thread)

    except Exception as e:
        logger.error(f"Failed to create thread: {e}")
        raise HTTPException(status_code=500, detail="Failed to create thread")

@router.get("/{thread_id}", response_model=ThreadRead)
async def get_thread(thread_id: str, db: AsyncSession = Depends(get_db)):
    logger.info(f"Fetching thread with id={thread_id}")
    
    try:
        thread = await thread_service.get_thread(db, thread_id)

        if thread is None:
            logger.warning(f"Thread not found: id={thread_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Thread not found"
            )

        logger.info(f"Thread retrieved: id={thread.id}")
        return ThreadRead.model_validate(thread)

    except HTTPException:
        raise 

    except Exception as e:
        logger.error(f"Error retrieving thread id={thread_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch thread")
    
@router.delete("/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_thread(thread_id: str, db: AsyncSession = Depends(get_db)):
    await thread_service.delete_thread(db, thread_id)

@router.patch("/{thread_id}", response_model=ThreadRead)
async def update_thread(
    thread_id: str,
    thread_data: ThreadCreate,
    db: AsyncSession = Depends(get_db)
):
    return ThreadRead.model_validate(
        await thread_service.update_thread(db, thread_id, thread_data)
    )
