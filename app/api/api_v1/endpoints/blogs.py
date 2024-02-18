from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api_v1.validators import check_blog_exists
from app.db.session import get_async_session
from app.crud import blog_crud, post_crud
from app.schemas import BlogView, PostCreate, PostView

router = APIRouter()


@router.get(
    path='/',
    response_model=list[BlogView],
    status_code=status.HTTP_200_OK
)
async def get_blogs(
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список всех блогов."""
    db_blogs = await blog_crud.get_multi(session)
    return db_blogs


@router.post(
    path='/{blog_id}/posts',
    response_model=PostView,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED
)
async def create_post(
    blog_id: int,
    obj_in: PostCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Создает новый пост в блоге."""
    await check_blog_exists(session=session, blog_id=blog_id)
    db_post = await post_crud.create(
        session=session, obj_in=obj_in, blog_id=blog_id)
    return db_post


@router.get(
    path='/{blog_id}/posts',
    response_model=Page[PostView],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK
)
async def get_posts_for_blog(
    blog_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> Page[PostView]:
    """Возвращает список всех постов блога с пагинацией."""
    await check_blog_exists(session=session, blog_id=blog_id)
    db_posts = await post_crud.get_multi_for_blog(
        session=session, blog_id=blog_id
    )
    return paginate(db_posts)
