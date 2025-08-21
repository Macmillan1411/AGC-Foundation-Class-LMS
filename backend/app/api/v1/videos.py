from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from app.schemas.video import VideoSchema
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.services.video_service import VideoService
from app.db.session import get_session
from app.core.deps import get_admin_user, get_current_user
from typing import List

video_router = APIRouter()
video_service = VideoService()


@video_router.get("/", response_model=List[VideoSchema])
async def get_all_videos(
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
    ):
    videos = await video_service.get_all_videos(session)
    return videos


@video_router.get("/{video_id}", response_model=VideoSchema)
async def get_video(
    video_id: str,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
    ) -> dict:

    video = await video_service.get_video_by_id(video_id, session)

    if video:
        return video
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )


@video_router.post("/", response_model=VideoSchema, status_code=status.HTTP_201_CREATED)
async def create_video(
    video: VideoSchema,
    session: AsyncSession = Depends(get_session),
    admin=Depends(get_admin_user)
    ) -> dict:

    created_video = await video_service.create_video(video, session)
    return created_video


@video_router.put("/{video_id}", response_model=VideoSchema)
async def update_video(
    video_id: str,
    video: VideoSchema,
    session: AsyncSession =  Depends(get_session),
    admin=Depends(get_admin_user)
    ) -> dict:
    
    updated_video = await video_service.update_video(video_id, video, session)

    if updated_video:
        return updated_video
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )


@video_router.delete("/{video_id}", response_model=VideoSchema)
async def delete_video(
    video_id: str,
    session: AsyncSession = Depends(get_session),
    admin=Depends(get_admin_user)
    ) -> dict:
    
    deleted_video = await video_service.delete_video(video_id, session)

    if deleted_video:
        return deleted_video
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Video not found"
        )
