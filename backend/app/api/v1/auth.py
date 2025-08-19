from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import UserService
from app.schemas.user import UserCreateSchema, UserSchema
from app.core.security import create_access_token, verify_password
from app.db.session import get_session

auth_router = APIRouter()
user_service = UserService()

@auth_router.post("/register", response_model=UserSchema)
async def register_user(user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    
    
    if await user_service.user_exists(user_data.email, session):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = await user_service.create_user(user_data, session)
    
    return UserSchema(id=new_user.id, email=new_user.email)


@auth_router.post("/login")
async def login_user(user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)):  
    user = await user_service.get_user_by_email(user_data.email, session)
    
    hashed_password = user.hashed_password if user else None

    if not user or not verify_password(user_data.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
     # Create token with minimal safe user data
    token_data = {
        "sub": user.email,  # Standard JWT subject identifier
        "user_id": str(user.id),  # Optional: include user ID
        "email": user.email
    }
    
    access_token = create_access_token(token_data)

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.get("/me", response_model=UserSchema)
async def get_me(current_user: UserSchema = Depends(get_session)):
    """Return the currently authenticated user's profile."""
    return current_user

