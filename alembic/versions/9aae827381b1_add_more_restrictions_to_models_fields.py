"""Add more restrictions to models fields.

Revision ID: 9aae827381b1
Revises: 7cbc6cbe21c1
Create Date: 2024-02-17 18:14:01.669645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9aae827381b1'
down_revision: Union[str, None] = '7cbc6cbe21c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('blogs', 'title',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('posts', 'blog_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('posts', 'title',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('readstatuses', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('readstatuses', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('subscriptions', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('subscriptions', 'blog_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('subscriptions', 'blog_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('subscriptions', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('readstatuses', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('readstatuses', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('posts', 'title',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    op.alter_column('posts', 'blog_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('blogs', 'title',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###
