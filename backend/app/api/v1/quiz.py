from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.quiz import QuizQuestionSchema, QuizSubmitRequest, QuizSubmitResponse
from app.services.quiz_service import QuizService
from app.db.session import get_session


quiz_router = APIRouter(tags=["quiz"])
quiz_service = QuizService()


@quiz_router.get("/", response_model=List[QuizQuestionSchema])
async def get_quizzes(video_id: int, session: AsyncSession = Depends(get_session), user=Depends(get_session)):
    quizzes = await quiz_service.get_quizzes_for_video(video_id, session)
    return quizzes


@quiz_router.post("/{quiz_id}", response_model=QuizSubmitResponse)
async def submit_quiz(
    quiz_id: int,
    request: QuizSubmitRequest,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_session)
):
    result = await quiz_service.check_answers(quiz_id, request.answers, session)
    return result
