from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_service import UserService
from app.schemas.user import UserCreateSchema, UserSchema, UserUpdateSchema
from app.core.security import create_access_token, verify_password
from app.db.session import get_session
from app.core.deps import get_current_user, get_admin_user

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

    return {"access_token": access_token}


@auth_router.get("/me", response_model=UserSchema)
async def get_me(current_user: UserSchema = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return UserSchema(
        email=current_user.email,
        is_admin=current_user.is_admin
    )


@auth_router.post("/admin/set_admin_status", response_model=UserUpdateSchema)
async def set_admin_status(email: str, is_admin: bool, current_user: UserSchema = Depends(get_admin_user), session: AsyncSession = Depends(get_session)):
    """Set a user's admin status."""
    user = await user_service.set_admin_status(email, is_admin, session)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserUpdateSchema(
        email=user.email,
        is_admin=user.is_admin
    )

@auth_router.delete("/admin/delete", response_model=UserSchema)
async def delete_user(email: str, current_user: UserSchema = Depends(get_admin_user), session: AsyncSession = Depends(get_session)):
    """Delete a user."""
    user = await user_service.delete_user(email, session)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserSchema(
        email=user.email,
        is_admin=user.is_admin
    )
