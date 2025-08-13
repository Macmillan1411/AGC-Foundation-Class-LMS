from fastapi import FastAPI
from app.api.v1.videos import video_router

app = FastAPI(title="AGC Foundation Class Learning API", version="1.0.0")

app.include_router(
    video_router,
    prefix="/api/v1/videos",
    tags=["videos"]
)