from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import blog_crud, user_crud


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


async def check_blog_exists(session: AsyncSession, blog_id: int):
    """Проверяет наличие блога в базе."""
    db_blog = await blog_crud.get(session=session, obj_id=blog_id)
    if not db_blog:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Блог с таким ID не найден'
        )
