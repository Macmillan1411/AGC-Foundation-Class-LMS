from app.db.models import User
from app.core.security import get_password_hash
from app.core.security import verify_password
from app.schemas.user import UserSchema, UserCreateSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.execute(statement)

        user = result.scalar_one_or_none()

        return user


    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False


    async def create_user(self, user_data: UserCreateSchema, session: AsyncSession):
        user_data_dict = user_data.model_dump(exclude={"password"})

        new_user = User(**user_data_dict)

        new_user.hashed_password = get_password_hash(user_data.password)

        session.add(new_user)

        await session.commit()

        return new_user
    
    async def delete_user(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        if not user:
            return None

        await session.delete(user)
        await session.commit()

        return user
    
    async def set_admin_status(self, email: str, is_admin: bool, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        if not user:
            return None

        user.is_admin = is_admin

        session.add(user)
        await session.commit()

        return user

    async def get_all_users(self, session: AsyncSession):
        statement = select(User)

        result = await session.execute(statement)

        users = result.scalars().all()

        return users