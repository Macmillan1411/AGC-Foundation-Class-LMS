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
        return [VideoSchema.from_orm(video) for video in videos]

    async def get_video_by_id(self, video_id: int, session: AsyncSession) -> Optional[VideoSchema]:
        query = select(Video).where(Video.id == video_id)
        result = await session.execute(query)
        video = result.scalar_one_or_none()
        return VideoSchema.from_orm(video) if video else None