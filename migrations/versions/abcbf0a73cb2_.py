"""empty message

Revision ID: abcbf0a73cb2
Revises: fc86fa9a2b44
Create Date: 2021-02-24 14:40:40.265658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abcbf0a73cb2'
down_revision = 'fc86fa9a2b44'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board_like', sa.Column('users_id', sa.Integer(), nullable=False))
    op.drop_constraint('board_like_board_id_fkey', 'board_like', type_='foreignkey')
    op.drop_constraint('board_like_user_id_fkey', 'board_like', type_='foreignkey')
    op.create_foreign_key(None, 'board_like', 'users', ['users_id'], ['id'])
    op.create_foreign_key(None, 'board_like', 'board', ['board_id'], ['id'])
    op.drop_column('board_like', 'user_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board_like', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'board_like', type_='foreignkey')
    op.drop_constraint(None, 'board_like', type_='foreignkey')
    op.create_foreign_key('board_like_user_id_fkey', 'board_like', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('board_like_board_id_fkey', 'board_like', 'board', ['board_id'], ['id'], ondelete='CASCADE')
    op.drop_column('board_like', 'users_id')
    # ### end Alembic commands ###
