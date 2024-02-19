from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import (
    blog_crud, post_crud, read_status_crud, subscription_crud, user_crud
)


async def check_username_or_email_exists(
    session: AsyncSession, username: str, email: str
):
    """Проверяет существование пользователя с таким именем или email."""
    db_users = await user_crud.get_by_username_or_email(
        session=session, username=username, email=email
    )
    if db_users:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Пользователь с таким именем или email уже существует'
        )


async def check_user_exists(session: AsyncSession, user_id: int):
    """Проверяет наличие пользователя в базе."""
    db_user = await user_crud.get_by_id(session=session, obj_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Пользователь с ID {user_id} не найден'
        )
    return db_user


async def check_blog_exists(session: AsyncSession, blog_id: int):
    """Проверяет наличие блога в базе."""
    db_blog = await blog_crud.get_by_id(session=session, obj_id=blog_id)
    if not db_blog:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Блог с ID {blog_id} не найден'
        )
    return db_blog


async def check_subscription_exists(
    session: AsyncSession, user_id: int, blog_id: int, delete: bool = False
):
    """
    Проверяет наличие подписки в базе. Не даёт создать или удалить повторно.
    """
    db_subscription = await subscription_crud.get(
        session=session, user_id=user_id, blog_id=blog_id
    )
    if db_subscription and not delete:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                f'Пользователь с ID {user_id} уже подписан на блог с ID '
                f'{blog_id}.'
            )
        )
    if not db_subscription and delete:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=(
                f'Подписка пользователя с ID {user_id} на блог с ID '
                f'{blog_id} не найдена.'
            )
        )
    return db_subscription


async def check_user_is_blog_owner(
        session: AsyncSession, user_id: int, blog_id: int
):
    """Проверяет, не является ли пользователь владельцем блога."""
    db_blog = await blog_crud.get_by_id(session=session, obj_id=blog_id)
    if db_blog.user_id == user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail=(
                f'Блог с ID {blog_id} пренадлежит пользователю с ID '
                f'{user_id}. Подписка на свой блог невозможна.'
            )
        )


async def check_post_exists(session: AsyncSession, post_id: int):
    """Проверяет наличие поста в базе."""
    db_post = await post_crud.get_by_id(session=session, obj_id=post_id)
    if not db_post:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Пост с ID {post_id} не найден'
        )
    return db_post


async def check_read_status_exists(
    session: AsyncSession, user_id: int, post_id: int, delete: bool = False
):
    """
    Проверяет наличие статуса прочтения в базе. Не даёт создать или удалить
    повторно.
    """
    db_read_status = await read_status_crud.get(
        session=session, user_id=user_id, post_id=post_id
    )
    if db_read_status and not delete:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                f'Пользователь с ID {user_id} уже прочитал пост с ID '
                f'{post_id}.'
            )
        )
    if not db_read_status and delete:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=(
                f'Статус прочтения пользователя с ID {user_id} поста с ID '
                f'{post_id} не найден.'
            )
        )
    return db_read_status
