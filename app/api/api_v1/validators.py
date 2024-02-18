from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import blog_crud, subscription_crud, user_crud


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
            detail='Пользователь с таким ID не найден'
        )


async def check_blog_exists(session: AsyncSession, blog_id: int):
    """Проверяет наличие блога в базе."""
    db_blog = await blog_crud.get_by_id(session=session, obj_id=blog_id)
    if not db_blog:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Блог с таким ID не найден'
        )


async def check_subscription_exists(
    session: AsyncSession, user_id: int, blog_id: int
):
    """Проверяет наличие подписки в базе."""
    db_subscription = await subscription_crud.get(
        session=session, user_id=user_id, blog_id=blog_id
    )
    if not db_subscription:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Подписка не найдена'
        )
    return db_subscription
