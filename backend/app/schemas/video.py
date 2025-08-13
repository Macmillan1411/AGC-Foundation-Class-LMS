from pydantic import BaseModel, Field
from typing import Optional, List


class VideoSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    url: str
    published: int  # 0 for not published, 1 for published
    order: int = 0  # Order for sorting videos
    
    class Config:
        from_attributes = True
