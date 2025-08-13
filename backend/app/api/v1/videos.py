from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from app.schemas.video import VideoSchema
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.services.video_service import VideoService
from app.db.session import get_session
from typing import List

video_router = APIRouter()
video_service = VideoService()


@video_router.get("/", response_model=List[VideoSchema])
async def get_all_videos(session: AsyncSession = Depends(get_session)):
    videos = await video_service.get_all_videos(session)
    return videos


@video_router.get("/{video_id}", response_model=VideoSchema)
async def get_video(video_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    video = await video_service.get_video_by_id(video_id, session)

    if video:
        return video
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )

