from fastapi import APIRouter, Depends, Response, status
from fastapi_pagination import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.validators import (
    check_blog_exists, check_post_exists, check_read_status_exists,
    check_subscription_exists, check_user_exists,
    check_user_is_blog_owner, check_username_or_email_exists
)
from app.crud import (
    blog_crud, post_crud, read_status_crud, subscription_crud, user_crud
)
from app.db.session import get_async_session
from app.models import User
from app.pagination import CustomPage as Page
from app.schemas import (
    BlogCreate, PostView, PostInFeed, ReadStatusCreate, ReadStatusView,
    SubscriptionCreate, SubscriptionView, UserCreate, UserView
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
) -> UserView:
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
) -> list[UserView]:
    """Возвращает список всех пользователей."""
    db_users = await user_crud.get_multi(session)
    return db_users


@router.post(
    path='/{user_id}/subscriptions',
    response_model=SubscriptionView,
    status_code=status.HTTP_201_CREATED,
    tags=['subscriptions']
)
async def subscribe_user_to_blog(
    user_id: int, obj_in: SubscriptionCreate,
    session: AsyncSession = Depends(get_async_session)
) -> SubscriptionView:
    """Создает подписку пользователя на блог."""
    await check_user_exists(session=session, user_id=user_id)
    blog_id = obj_in.blog_id
    await check_blog_exists(session=session, blog_id=blog_id)
    await check_subscription_exists(
        session=session, user_id=user_id, blog_id=blog_id,
        delete=False
    )
    await check_user_is_blog_owner(
        session=session, user_id=user_id, blog_id=blog_id
    )
    db_subscription = await subscription_crud.create(
        session=session, obj_in=obj_in, user_id=user_id
    )
    return db_subscription


@router.delete(
    path='/{user_id}/subscriptions/{blog_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['subscriptions']
)
async def unsubscribe_user_from_blog(
    user_id: int, blog_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Response:
    """Удаляет подписку пользователя на блог."""
    await check_user_exists(session=session, user_id=user_id)
    await check_blog_exists(session=session, blog_id=blog_id)
    db_obj = await check_subscription_exists(
        session=session, user_id=user_id, blog_id=blog_id,
        delete=True
    )
    await subscription_crud.remove(session, db_obj)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    path='/{user_id}/subscriptions',
    response_model=list[SubscriptionView],
    status_code=status.HTTP_200_OK,
    tags=['subscriptions']
)
async def get_user_subscriptions(
    user_id: int, session: AsyncSession = Depends(get_async_session)
) -> list[SubscriptionView]:
    """Возвращает список подписок пользователя на блоги."""
    await check_user_exists(session=session, user_id=user_id)
    db_objs = await subscription_crud.get_multi_for_user(session, user_id)
    return db_objs


@router.post(
    path='/{user_id}/read-posts',
    response_model=ReadStatusView,
    status_code=status.HTTP_201_CREATED,
    tags=['posts read status']
)
async def mark_post_as_read_by_user(
    user_id: int, obj_in: ReadStatusCreate,
    session: AsyncSession = Depends(get_async_session)
) -> ReadStatusView:
    """Создает запись о прочитанном пользователем посте."""
    await check_user_exists(session=session, user_id=user_id)
    post_id = obj_in.post_id
    await check_post_exists(session=session, post_id=post_id)
    await check_read_status_exists(
        session=session, user_id=user_id, post_id=post_id, delete=False
    )
    db_read_status = await read_status_crud.create(
        session=session, obj_in=obj_in, user_id=user_id
    )
    return db_read_status


@router.delete(
    path='/{user_id}/read-posts/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['posts read status']
)
async def unmark_post_as_read_by_user(
    user_id: int, post_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Response:
    """Удаляет запись о прочитанном пользователем посте."""
    await check_user_exists(session=session, user_id=user_id)
    await check_post_exists(session=session, post_id=post_id)
    db_obj = await check_read_status_exists(
        session=session, user_id=user_id, post_id=post_id, delete=True
    )
    await read_status_crud.remove(session, db_obj)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    path='/{user_id}/read-posts',
    response_model=list[ReadStatusView],
    status_code=status.HTTP_200_OK,
    tags=['posts read status']
)
async def get_user_read_statuses(
    user_id: int, session: AsyncSession = Depends(get_async_session)
) -> list[ReadStatusView]:
    """Возвращает список записей о прочитанных пользователем постах."""
    await check_user_exists(session=session, user_id=user_id)
    db_objs = await read_status_crud.get_multi_for_user(session, user_id)
    return db_objs


@router.get(
    path='/{user_id}/feed',
    response_model=Page[PostInFeed],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    tags=['feed']
)
async def get_user_feed(
    user_id: int, session: AsyncSession = Depends(get_async_session),
    unread: bool = True, read: bool = True
) -> Page[PostView]:
    """
    Возвращает ленту пользователя с возможностью пагинации и фильтрации по
    непрочитанным и прочитанным постам.
    """
    await check_user_exists(session=session, user_id=user_id)
    if unread and read:
        db_objs = await post_crud.get_multi_for_user_feed(session, user_id)
    elif unread:
        db_objs = await post_crud.get_multi_unread_for_user_feed(
            session, user_id
        )
    elif read:
        db_objs = await post_crud.get_multi_read_for_user_feed(
            session, user_id
        )
    else:
        db_objs = []
    return paginate(db_objs)


async def _create_first_blog_for_user(
    user: User, session: AsyncSession
) -> None:
    """
    Создает первый блог для пользователя после создания самого пользователя.
    """
    obj_in = BlogCreate(
        user_id=user.id, title=f'Блог пользователя {user.username}'
    )
    await blog_crud.create(session, obj_in)
