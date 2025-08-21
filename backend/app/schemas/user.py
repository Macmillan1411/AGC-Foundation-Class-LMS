from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserSchema(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")

    class Config:
        from_attributes = True

class UserCreateSchema(UserSchema):
    password: str = Field(..., min_length=8, example="strongpassword123")
