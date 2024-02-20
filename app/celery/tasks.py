from app.db.session import AsyncSessionLocal
from app.config import constants
from app.crud import post_crud, user_crud
from app.models import Post, User


async def _get_all_users() -> list[User]:
    """Возвращает всех пользователей из базы."""
    async with AsyncSessionLocal() as session:
        users = await user_crud.get_multi(session)
        return users


async def _get_users_feed(user_id: int) -> list[Post]:
    """Возвращает ленту постов пользователя."""
    async with AsyncSessionLocal() as session:
        feed = await post_crud.get_multi_for_user_feed(
            session=session, user_id=user_id,
            limit=constants.POSTS_PER_EMAIL
        )
        return feed


async def send_email_to_users_with_feed() -> None:
    """
    Отправляет email пользователям с """
    users = await _get_all_users()
    for user in users:
        feed = await _get_users_feed(user.id)
        if feed:
            # Отправка email
            print(
                f'Отправка email для пользователя {user.username} '
                f'по адресу {user.email} с {len(feed)} последними постами'
            )
            print('Список постов:')
            for post in feed:
                print(f'  {post.title}')
        else:
            print(
                f'Пользователь {user.email} ни на кого не подписан. Email не '
                'отправлен.'
            )
    print('Все email отправлены.')
