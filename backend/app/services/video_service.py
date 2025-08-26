from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, desc
from app.db.models.videos import Video
from app.schemas.video import VideoSchema
from typing import List, Optional


class VideoService:

    async def get_all_videos(self, session: AsyncSession, published: bool = True) -> List[VideoSchema]:
        query = select(Video).where(Video.published == 1).order_by(desc(Video.order))
        result = await session.execute(query)
        videos = result.scalars().all()
        return [VideoSchema.model_validate(video) for video in videos]

    async def get_video_by_id(self, video_id: int, session: AsyncSession) -> Optional[VideoSchema]:
        query = select(Video).where(Video.id == video_id)
        result = await session.execute(query)
        video = result.scalar_one_or_none()
        return VideoSchema.model_validate(video) if video else None
    
    async def create_video(self, video_data: VideoSchema, session: AsyncSession) -> VideoSchema:
        new_video = Video(**video_data.model_dump())
        session.add(new_video)
        await session.commit()
        await session.refresh(new_video)
        return VideoSchema.model_validate(new_video)
    
    async def delete_video(self, video_id: int, session: AsyncSession) -> Optional[VideoSchema]:
        video = await self.get_video_by_id(video_id, session)
        if not video:
            return None
        await session.delete(video)
        await session.commit()
        return video
    
    async def update_video(self, video_id: int, video_data: VideoSchema, session: AsyncSession) -> Optional[VideoSchema]:
        video = await self.get_video_by_id(video_id, session)
        if not video:
            return None
        for key, value in video_data.model_dump().items():
            setattr(video, key, value)
        session.add(video)
        await session.commit()
        await session.refresh(video)
        return VideoSchema.model_validate(video)
