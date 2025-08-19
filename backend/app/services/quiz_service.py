from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.quiz import QuizQuestion, QuizOption

class QuizService:
    async def get_quizzes_for_video(self, video_id: int, session: AsyncSession):
        stmt = select(QuizQuestion).where(QuizQuestion.video_id == video_id)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def check_answers(self, quiz_id: int, answers: list[int], session: AsyncSession):
        stmt = select(QuizOption).where(QuizOption.question_id == quiz_id)
        result = await session.execute(stmt)
        options = result.scalars().all()

        correct_ids = [opt.id for opt in options if opt.is_correct]
        score = int((len(set(answers) & set(correct_ids)) / len(correct_ids)) * 100) if correct_ids else 0

        is_passed = score >= 70
        message = "Quiz passed. Next video unlocked!" if is_passed else "Quiz failed. Try again."

        return {"score": score, "is_passed": is_passed, "message": message}
