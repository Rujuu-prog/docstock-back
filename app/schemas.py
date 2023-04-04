from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None


class GroupCreate(GroupBase):
    creator_id: int


class Group(GroupBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    name: str


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


class DocumentBase(BaseModel):
    title: str
    content: Optional[str] = None


class DocumentCreate(DocumentBase):
    pass


class Document(DocumentBase):
    id: int
    created_at: datetime
    owner_id: int
    group_id: int

    class Config:
        orm_mode = True


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True
