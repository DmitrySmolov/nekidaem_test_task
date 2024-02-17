from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.config import constants as const


class User(Base):
    """Модель пользователя."""
    username = Column(
        String(const.TITLE_MAX_LENGTH), unique=True, nullable=False
    )
    email = Column(
        String(const.EMAIL_MAX_LENGTH), unique=True, nullable=False
    )
    first_name = Column(
        String(const.TITLE_MAX_LENGTH), nullable=False
    )
    last_name = Column(
        String(const.TITLE_MAX_LENGTH), nullable=False
    )

    blogs = relationship('Blog', back_populates='user')
    subscriptions = relationship(
        'Subscription', back_populates='user', cascade='all, delete'
    )
    read_statuses = relationship(
        'ReadStatus', back_populates='user', cascade='all, delete'
    )

    def __str__(self) -> str:
        return f'Польователь {self.username}'


class Blog(Base):
    """
    Модель блога пользователя. Не смотря на условие "один пользователь - один
    блог", блог выведен в отдельную модель для возможности расширения (
    например, если в будущем будет поддержка нескольких блогов).
    """
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    title = Column(String(const.TITLE_MAX_LENGTH), nullable=False)

    posts = relationship('Post', back_populates='blog', cascade='all, delete')
    subscriptions = relationship(
        'Subscription', back_populates='blog', cascade='all, delete'
    )

    def __str__(self) -> str:
        return f'Блог "{self.title}" пользователя {self.user.username}'


class Post(Base):
    """Модель поста в блоге."""
    blog_id = Column(
        Integer, ForeignKey('blogs.id'), nullable=False
    )
    title = Column(String(const.TITLE_MAX_LENGTH), nullable=False)
    content = Column(String(const.CONTENT_MAX_LENGTH))

    read_statuses = relationship(
        'ReadStatus', back_populates='post', cascade='all, delete'
    )

    def __str__(self) -> str:
        return f'Пост "{self.title}" в блоге {self.blog.title}'


class Subscription(Base):
    """Модель подпписки пользователя на блог."""
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    blog_id = Column(Integer, ForeignKey('blogs.id'), nullable=False)

    def __str__(self) -> str:
        return (
            f'Подписка пользователя {self.user.username} на блог ' +
            self.blog.title
        )


class ReadStatus(Base):
    """Модель статуса прочтения поста пользователем."""
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)

    def __str__(self) -> str:
        return (
            f'Статус прочтения поста "{self.post.title}" пользователем ' +
            self.user.username
        )
