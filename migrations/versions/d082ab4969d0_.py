"""empty message

Revision ID: d082ab4969d0
Revises: 6a3b106a9f8e
Create Date: 2021-02-20 23:47:58.966532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd082ab4969d0'
down_revision = '6a3b106a9f8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('store',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('phone_num', sa.String(length=255), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('profile_img', sa.String(length=1000), nullable=True),
    sa.Column('profile_detail', sa.String(), nullable=True),
    sa.Column('working_time', sa.String(length=255), nullable=False),
    sa.Column('break_day', sa.String(length=50), nullable=True),
    sa.Column('open_or_not', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('store_like',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('store_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['store_id'], ['store.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'store_id')
    )
    op.create_table('board_like',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['board_id'], ['board.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'board_id')
    )
    op.add_column('board', sa.Column('content', sa.String(length=300), nullable=False))
    op.drop_column('board', 'comment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board', sa.Column('comment', sa.VARCHAR(length=300), autoincrement=False, nullable=False))
    op.drop_column('board', 'content')
    op.drop_table('board_like')
    op.drop_table('store_like')
    op.drop_table('store')
    # ### end Alembic commands ###
