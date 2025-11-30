import logging
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from time import time
from framework.database import Base, engine
from resources.thread_resource import router as thread_router
from resources.message_resource import router as message_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | messaging-ms | %(message)s",
)

logger = logging.getLogger("messaging-ms")
logger.info("Messaging Microservice starting...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialization complete.")
    yield
    logger.info("Messaging Microservice shutting down.")


app = FastAPI(
    title="Messaging Microservice",
    description="Handles messaging and threads for the Neighborhood Exchange app",
    version="1.0.0",
    lifespan=lifespan,
)

# Logs every request hitting this microservice

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time()

    response = await call_next(request)
    duration = round((time() - start) * 1000, 2)

    logger.info(
        f"{request.method} {request.url.path} "
        f"completed_in={duration}ms "
        f"status={response.status_code}"
    )

    return response

app.include_router(thread_router)
app.include_router(message_router)


@app.get("/")
async def root():
    logger.info("Root endpoint called.")
    return {"message": "Messaging microservice is running!"}


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("FASTAPIPORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
