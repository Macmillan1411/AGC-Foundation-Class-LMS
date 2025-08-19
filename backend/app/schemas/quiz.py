from pydantic import BaseModel
from typing import List

class QuizOptionSchema(BaseModel):
    id: int
    option_text: str

    class Config:
        from_attributes = True


class QuizQuestionSchema(BaseModel):
    id: int
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
