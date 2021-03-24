"""empty message

Revision ID: 1efe014ad2de
Revises: abcbf0a73cb2
Create Date: 2021-02-24 15:04:06.295842

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1efe014ad2de'
down_revision = 'abcbf0a73cb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board_like', sa.Column('user_id', sa.Integer(), nullable=False))
    op.drop_constraint('board_like_board_id_fkey', 'board_like', type_='foreignkey')
    op.drop_constraint('board_like_users_id_fkey', 'board_like', type_='foreignkey')
    op.create_foreign_key(None, 'board_like', 'board', ['board_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'board_like', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('board_like', 'users_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board_like', sa.Column('users_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'board_like', type_='foreignkey')
    op.drop_constraint(None, 'board_like', type_='foreignkey')
    op.create_foreign_key('board_like_users_id_fkey', 'board_like', 'users', ['users_id'], ['id'])
    op.create_foreign_key('board_like_board_id_fkey', 'board_like', 'board', ['board_id'], ['id'])
    op.drop_column('board_like', 'user_id')
    # ### end Alembic commands ###
