from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import constants as const
from app.models import Blog, Post, ReadStatus, Subscription, User


class CRUDBase:
    """Базовый класс для CRUD-операций с моделями."""
    def __init__(self, model):
        self.model = model

    async def get(self, session: AsyncSession, obj_id: int):
        """Возвращает объект по его ID."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalar().first()

    async def get_multi(
        self, session: AsyncSession,
        skip: int = 0, limit: int = const.MAX_POSTS_IN_FEED
    ):
        """Возвращает список объектов."""
        db_objs = await session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return db_objs.scalars().all()

    async def create(self, session: AsyncSession, obj_in):
        """Создает новый объект."""
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


class PostCRUD(CRUDBase):
    """Класс для CRUD-операций с постами."""

    @staticmethod
    def _get_unread_posts_ids_query(user_id: int):
        """Возвращает запрос для получения ID непрочитанных постов."""
        return select(ReadStatus.post_id).where(ReadStatus.user_id == user_id)

    async def get_multi_for_user_feed(
        self, session: AsyncSession, user_id: int,
        skip: int = 0, limit: int = const.POSTS_PER_PAGE
    ):
        """Возвращает посты для ленты пользователя."""
        statement = (
            select(self.model).select_from(
                self.model, Subscription,
                self.model.blog_id == Subscription.blog_id
            ).where(
                Subscription.user_id == user_id
            ).offset(skip).limit(limit)
        )
        db_objs = await session.execute(statement)
        return db_objs.scalars().all()

    async def get_multi_unread_for_user_feed(
        self, session: AsyncSession, user_id: int,
        skip: int = 0, limit: int = const.MAX_POSTS_IN_FEED
    ):
        """Возвращает прочитанные посты для ленты пользователя."""
        read_posts_ids = self._get_unread_posts_ids_query(user_id)
        statement = (
            select(self.model).select_from(
                self.model, Subscription,
                self.model.blog_id == Subscription.blog_id
            ).where(
                Subscription.user_id == user_id,
                self.model.id.notin_(read_posts_ids)
            ).offset(skip).limit(limit)
        )
        db_objs = await session.execute(statement)
        return db_objs.scalars().all()

    async def get_multi_read_for_user_feed(
        self, session: AsyncSession, user_id: int,
        skip: int = 0, limit: int = const.MAX_POSTS_IN_FEED
    ):
        """Возвращает прочитанные посты для ленты пользователя."""
        read_posts_ids = self._get_unread_posts_ids_query(user_id)
        statement = (
            select(self.model).select_from(
                self.model, Subscription,
                self.model.blog_id == Subscription.blog_id
            ).where(
                Subscription.user_id == user_id,
                self.model.id.in_(read_posts_ids)
            ).offset(skip).limit(limit)
        )
        db_objs = await session.execute(statement)
        return db_objs.scalars().all()


class RemoveMixin:
    """Миксин для удаления объектов."""
    async def remove(self, session: AsyncSession, db_obj):
        """Удаляет объект."""
        session.delete(db_obj)
        await session.commit()
        return db_obj


class SubscriptionAndReadStatusCRUD(CRUDBase, RemoveMixin):
    """Класс для CRUD-операций с подписками и статусом прочтения."""
    pass


user_crud = CRUDBase(User)
blog_crud = CRUDBase(Blog)
post_crud = PostCRUD(Post)
subscription_crud = SubscriptionAndReadStatusCRUD(Subscription)
read_status_crud = SubscriptionAndReadStatusCRUD(ReadStatus)
