from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from app.config import constants as const


class ViewMixin:
    """Миксин для отображения объектов."""
    id: int
    created_at: datetime


class UserCreate(BaseModel):
    """Схема для создания нового пользователя."""
    username: Annotated[str, Field(max_length=const.TITLE_MAX_LENGTH)]
    email: EmailStr
    first_name: Annotated[str, Field(max_length=const.TITLE_MAX_LENGTH)]
    last_name: Annotated[str, Field(max_length=const.TITLE_MAX_LENGTH)]

    class Config:
        orm_mode = True


class UserView(ViewMixin, UserCreate):
    """Схема для отображения пользователя."""
    pass


class BlogCreate(BaseModel):
    """Схема для создания блога."""
    user_id: int
    title: Annotated[str, Field(max_length=const.TITLE_MAX_LENGTH)]

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    """Схема для создания поста."""
    blog_id: int
    title: Annotated[str, Field(max_length=const.TITLE_MAX_LENGTH)]
    content: Annotated[str, Field(max_length=const.CONTENT_MAX_LENGTH)] | None

    class Config:
        orm_mode = True


class PostView(ViewMixin, PostCreate):
    """Схема для отображения поста."""
    pass


class SubscriptionCreate(BaseModel):
    """Схема для создания подписки пользователя на блог."""
    user_id: int
    blog_id: int

    class Config:
        orm_mode = True


class ReadStatusCreate(BaseModel):
    """Схема для создания записи о прочитанном пользователем посте."""
    user_id: int
    post_id: int

    class Config:
        orm_mode = True
