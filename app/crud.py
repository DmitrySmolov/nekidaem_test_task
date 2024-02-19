from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Blog, Post, ReadStatus, Subscription, User


class CRUDBase:
    """Базовый класс для CRUD-операций с моделями."""
    def __init__(self, model):
        self.model = model

    async def get_by_id(self, session: AsyncSession, obj_id: int):
        """Возвращает объект по его ID."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        """
        Возвращает список объектов в обратном хронологическом порядке
        времени их создания.
        """
        db_objs = await session.execute(
            select(self.model).order_by(
                desc(self.model.created_at)
            )
        )
        return db_objs.scalars().all()

    async def create(self, session: AsyncSession, obj_in: BaseModel, **kwargs):
        """Создает новый объект."""
        obj_in_data = obj_in.model_dump()
        obj_in_data.update(kwargs)
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


class UserCRUD(CRUDBase):
    """Класс для CRUD-операций с пользователями."""

    async def get_by_username_or_email(
        self, session: AsyncSession, username: str, email: str
    ):
        """Возвращает пользователей из базы по его имени или email."""
        db_user = await session.execute(
            select(self.model).where(
                (self.model.username == username) |
                (self.model.email == email)
            )
        )
        return db_user.scalars().all()


class RemoveMixin:
    """Миксин для удаления объектов."""
    async def remove(self, session: AsyncSession, db_obj):
        """Удаляет объект."""
        await session.delete(db_obj)
        await session.commit()


class PostCRUD(CRUDBase, RemoveMixin):
    """Класс для CRUD-операций с постами."""

    @staticmethod
    def _get_base_query_for_user_feed(user_id: int):
        """
        Возвращает базовый запрос для получения постов для ленты в обратном
        хронологическом порядке их создания.
        """
        return select(Post).join(
            Subscription, Post.blog_id == Subscription.blog_id
        ).where(Subscription.user_id == user_id).order_by(
            desc(Post.created_at)
        )

    @staticmethod
    async def _get_read_posts_ids(
        session: AsyncSession, user_id: int
    ) -> list[int]:
        """Возвращает список ID прочитанных пользователем постов."""
        statement = select(ReadStatus.post_id).where(
            ReadStatus.user_id == user_id
        )
        result = await session.execute(statement)
        return result.scalars().all()

    async def get_multi_for_user_feed(
        self, session: AsyncSession, user_id: int
    ):
        """Возвращает все посты для ленты пользователя."""
        statement = self._get_base_query_for_user_feed(user_id)
        db_objs = await session.execute(statement)
        return db_objs.scalars().all()

    async def get_multi_unread_for_user_feed(
        self, session: AsyncSession, user_id: int
    ):
        """Возвращает непрочитанные посты для ленты пользователя."""
        read_posts_ids = await self._get_read_posts_ids(session, user_id)
        base_query = self._get_base_query_for_user_feed(user_id)
        statement = base_query.where(
            self.model.id.notin_(read_posts_ids)
        )
        db_objs = await session.execute(statement)
        return db_objs.scalars().all()

    async def get_multi_read_for_user_feed(
        self, session: AsyncSession, user_id: int
    ):
        """Возвращает прочитанные посты для ленты пользователя."""
        read_posts_ids = await self._get_read_posts_ids(session, user_id)
        base_query = self._get_base_query_for_user_feed(user_id)
        statement = base_query.where(
            self.model.id.in_(read_posts_ids)
        )
        db_objs = await session.execute(statement)
        return db_objs.scalars().all()

    async def get_multi_for_blog(
        self, session: AsyncSession, blog_id: int
    ):
        """Возвращает посты данного блога."""
        db_objs = await session.execute(
            select(self.model).where(
                self.model.blog_id == blog_id
            ).order_by(desc(self.model.created_at))
        )
        return db_objs.scalars().all()


class UserToObjRelationsMixin:
    """
    Миксин для извлечения объектов из базы по ID пользователя для моделей
    Subscription и ReadStatus.
    """

    async def get_multi_for_user(
        self, session: AsyncSession, user_id: int
    ):
        """Возвращает список объектов из базы по ID пользователя."""
        db_objs = await session.execute(
            select(self.model).where(self.model.user_id == user_id).order_by(
                desc(self.model.created_at)
            )
        )
        return db_objs.scalars().all()


class SubscriptionCRUD(
    CRUDBase, RemoveMixin, UserToObjRelationsMixin
):
    """Класс для CRUD-операций с подписками."""

    async def get(
        self, session: AsyncSession, user_id: int, blog_id: int
    ):
        """Возвращает подписку из базы по ID пользователя и блога."""
        db_obj = await session.execute(
            select(self.model).where(
                (self.model.user_id == user_id) &
                (self.model.blog_id == blog_id)
            )
        )
        return db_obj.scalars().first()


class ReadStatusCRUD(
    CRUDBase, RemoveMixin, UserToObjRelationsMixin
):
    """Класс для CRUD-операций со статусами прочтения постов."""

    async def get(
        self, session: AsyncSession, user_id: int, post_id: int
    ):
        """Возвращает статус прочтения из базы по ID пользователя и поста."""
        db_obj = await session.execute(
            select(self.model).where(
                (self.model.user_id == user_id) &
                (self.model.post_id == post_id)
            )
        )
        return db_obj.scalars().first()


user_crud = UserCRUD(User)
blog_crud = CRUDBase(Blog)
post_crud = PostCRUD(Post)
subscription_crud = SubscriptionCRUD(Subscription)
read_status_crud = ReadStatusCRUD(ReadStatus)
