from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.quiz import QuizQuestion, QuizOption
from app.schemas.quiz import QuizQuestionSchema, QuizOptionSchema

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
    
    async def create_quiz_for_video(self, question: QuizQuestionSchema, session: AsyncSession):
        new_question = QuizQuestion(video_id=question.video_id, question_text=question.question_text)
        session.add(new_question)
        await session.commit()
        await session.refresh(new_question)

        for option in question.options:
            new_option = QuizOption(question_id=new_question.id, option_text=option.option_text)
            session.add(new_option)

        await session.commit()
        return new_question
    
    async def delete_quiz(self, quiz_id: int, session: AsyncSession):
        stmt = select(QuizQuestion).where(QuizQuestion.id == quiz_id)
        result = await session.execute(stmt)
        quiz = result.scalar_one_or_none()

        if not quiz:
            return None

        await session.delete(quiz)
        await session.commit()
        return quiz
    
    async def update_quiz(self, quiz_id: int, question: QuizQuestionSchema, session: AsyncSession):
        stmt = select(QuizQuestion).where(QuizQuestion.id == quiz_id)
        result = await session.execute(stmt)
        quiz = result.scalar_one_or_none()

        if not quiz:
            return None

        quiz.question_text = question.question_text
        await session.commit()
        await session.refresh(quiz)

        # Update options
        for option in question.options:
            option_stmt = select(QuizOption).where(
                QuizOption.question_id == quiz_id,
                QuizOption.option_text == option.option_text
            )
            option_result = await session.execute(option_stmt)
            existing_option = option_result.scalar_one_or_none()

            if existing_option:
                existing_option.option_text = option.option_text
            else:
                new_option = QuizOption(question_id=quiz.id, option_text=option.option_text)
                session.add(new_option)

        await session.commit()
        return quiz
