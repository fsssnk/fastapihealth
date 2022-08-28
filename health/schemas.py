from pydantic import BaseModel
from .database import Base
from typing import List


class PostBase(BaseModel):
    title: str
    body: str


class Post(PostBase):

    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    posts: List[Post] = []

    class Config():
        orm_mode = True


class ShowPost(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config():
        orm_mode = True