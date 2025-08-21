from pydantic import BaseModel
from typing import List, Optional

class QuizOptionSchema(BaseModel):
    id: Optional[int] = None
    option_text: str

    class Config:
        from_attributes = True


class QuizQuestionSchema(BaseModel):
    id: Optional[int] = None
    question_text: str
    options: List[QuizOptionSchema]

    class Config:
        from_attributes = True


class QuizSubmitRequest(BaseModel):
    answers: List[int]


class QuizSubmitResponse(BaseModel):
    score: int
    is_passed: bool
    message: str
