from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.base_class import Base


class User(Base):
    """Модель пользователя."""
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)


class Blog(Base):
    """Модель блога пользователя."""
    user_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String)


class Post(Base):
    """Модель поста в блоге."""
    blog_id = Column(Integer, ForeignKey('blog.id'))
    title = Column(String)
    content = Column(String(length=140))


class Subscription(Base):
    """Модель подпписки пользователя на блог."""
    user_id = Column(Integer, ForeignKey('user.id'))
    blog_id = Column(Integer, ForeignKey('blog.id'))


class ReadStatus(Base):
    """Модель статуса прочтения поста пользователем."""
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
