from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.validators import (
    check_blog_exists, check_subscription_exists, check_user_exists,
    check_username_or_email_exists
)
from app.db.session import get_async_session
from app.crud import blog_crud, subscription_crud, user_crud
from app.models import User
from app.schemas import (
    BlogCreate, SubscriptionCreate, SubscriptionView, UserCreate, UserView
)

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


@router.post(
    path='/{user_id}/subscriptions',
    response_model=SubscriptionView,
    status_code=status.HTTP_201_CREATED
)
async def subscribe_user_to_blog(
    user_id: int, obj_in: SubscriptionCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создает подписку пользователя на блог."""
    await check_user_exists(session=session, user_id=user_id)
    blog_id = obj_in.blog_id
    await check_blog_exists(session=session, blog_id=blog_id)
    db_subscription = await subscription_crud.create(
        session=session, obj_in=obj_in, user_id=user_id
    )
    return db_subscription


@router.delete(
    path='/{user_id}/subscriptions/{blog_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def unsubscribe_user_from_blog(
    user_id: int, blog_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Удаляет подписку пользователя на блог."""
    await check_user_exists(session=session, user_id=user_id)
    await check_blog_exists(session=session, blog_id=blog_id)
    db_obj = await check_subscription_exists(
        session=session, user_id=user_id, blog_id=blog_id
    )
    return await subscription_crud.remove(session, db_obj)


@router.get(
    path='/{user_id}/subscriptions',
    response_model=list[SubscriptionView],
    status_code=status.HTTP_200_OK
)
async def get_user_subscriptions(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список подписок пользователя на блоги."""
    await check_user_exists(session=session, user_id=user_id)
    db_objs = await subscription_crud.get_multi_for_user(session, user_id)
    return db_objs


async def _create_first_blog_for_user(
    user: User, session: AsyncSession
):
    """Создает первый блог для пользователя."""
    obj_in = BlogCreate(
        user_id=user.id, title=f'Блог пользователя {user.username}'
    )
    await blog_crud.create(session, obj_in)
