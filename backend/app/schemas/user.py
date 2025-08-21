from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserSchema(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")

    class Config:
        from_attributes = True

class UserCreateSchema(UserSchema):
    password: str = Field(..., min_length=8, example="strongpassword123")


class UserUpdateSchema(UserSchema):
    is_admin: Optional[bool] = Field(None, example=True)

    class Config:
        from_attributes = True
