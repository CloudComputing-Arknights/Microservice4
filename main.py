from __future__ import annotations
import os
from fastapi import FastAPI
from framework.database import Base, engine
from resources.thread_resource import router as thread_router
from resources.message_resource import router as message_router

port = int(os.environ.get("FASTAPIPORT", 8000))
app = FastAPI(
    title="Messaging Microservice",
    description="Handles messaging and threads for the Neighborhood Exchange app",
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)
app.include_router(message_router)
app.include_router(thread_router)


# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Messaging microservice is running!"}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
