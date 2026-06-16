from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.video import router as video_router
from app.routes.chat import router as chat_router

app = FastAPI(
    title="YouTube RAG API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "YouTube RAG Running"
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Video Routes
app.include_router(video_router)

# Chat Routes
app.include_router(chat_router)