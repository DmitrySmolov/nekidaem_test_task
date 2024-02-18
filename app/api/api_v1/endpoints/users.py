from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.validators import check_username_or_email_exists
from app.db.session import get_async_session
from app.crud import blog_crud, user_crud
from app.models import User
from app.schemas import BlogCreate, UserCreate, UserView

router = APIRouter()


@router.post(
    path='/',
    response_model=UserView,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    obj_in: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создает нового пользователя и его блог."""
    username = obj_in.username
    email = obj_in.email
    await check_username_or_email_exists(
        session=session, username=username, email=email
    )
    db_user = await user_crud.create(session, obj_in)
    if db_user:
        await _create_first_blog_for_user(db_user, session)
    return db_user


@router.get(
    path='/',
    response_model=list[UserView],
    status_code=status.HTTP_200_OK
)
async def get_users(
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список всех пользователей."""
    db_users = await user_crud.get_multi(session)
    return db_users


async def _create_first_blog_for_user(
    user: User, session: AsyncSession
):
    """Создает первый блог для пользователя."""
    obj_in = BlogCreate(
        user_id=user.id, title=f'Блог пользователя {user.username}'
    )
    await blog_crud.create(session, obj_in)
