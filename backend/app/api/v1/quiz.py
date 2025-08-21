from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.quiz import QuizQuestionSchema, QuizSubmitRequest, QuizSubmitResponse, QuizOptionSchema
from app.services.quiz_service import QuizService
from app.db.session import get_session
from app.core.deps import get_admin_user, get_current_user


quiz_router = APIRouter(tags=["quiz"])
quiz_service = QuizService()


@quiz_router.get("/", response_model=List[QuizQuestionSchema])
async def get_quizzes(
    video_id: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    quizzes = await quiz_service.get_quizzes_for_video(video_id, session)
    return quizzes


@quiz_router.post("/{quiz_id}", response_model=QuizSubmitResponse)
async def submit_quiz(
    quiz_id: int,
    request: QuizSubmitRequest,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    result = await quiz_service.check_answers(quiz_id, request.answers, session)
    return result


@quiz_router.post("/create", response_model=QuizQuestionSchema)
async def create_quiz(
    question: QuizQuestionSchema,
    session: AsyncSession = Depends(get_session),
    admin=Depends(get_admin_user)
):
    """Create a new quiz question (Admin only)."""
    if admin is None:
        raise HTTPException(status_code=403, detail="Only admins can create quizzes")
    new_quiz = await quiz_service.create_quiz_for_video(question, session)
    return new_quiz


@quiz_router.delete("/{quiz_id}", response_model=QuizQuestionSchema)
async def delete_quiz(
    quiz_id: int,
    session: AsyncSession = Depends(get_session),
    admin=Depends(get_admin_user)
):
    """Delete a quiz question(Admin only)."""
    
    if admin is None:
        raise HTTPException(status_code=403, detail="Only admins can delete quizzes")
    
    deleted_quiz = await quiz_service.delete_quiz(quiz_id, session)
    
    if not deleted_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")


@quiz_router.put("/{quiz_id}", response_model=QuizQuestionSchema)
async def update_quiz(
    quiz_id: int,
    question: QuizQuestionSchema,
    session: AsyncSession = Depends(get_session),
    admin=Depends(get_admin_user)
):
    """Update a quiz question (Admin only)."""
    if admin is None:
        raise HTTPException(status_code=403, detail="Only admins can update quizzes")
    updated_quiz = await quiz_service.update_quiz(quiz_id, question, session)
    if not updated_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return updated_quiz