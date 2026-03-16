from pydantic import BaseModel
from typing import Optional
from datetime import datetime
# This defines what data the CLIENT sends TO you
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

# This defines what data YOU send BACK to the client
# Notice: no password field — never send passwords back!
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode=True

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    created_at: datetime

    class Config:
        orm_mode=True

class FollowCreate(BaseModel):
    following_id:int

class FollowResponse(BaseModel):
    id: int
    follower_id: int
    following_id: int
    created_at: datetime
