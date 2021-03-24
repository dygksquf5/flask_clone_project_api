"""empty message

Revision ID: ee0585848c1a
Revises: 0e608bee8ef2
Create Date: 2021-02-21 12:19:16.450535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee0585848c1a'
down_revision = '0e608bee8ef2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board', sa.Column('content', sa.String(length=300), nullable=False))
    op.drop_column('board', 'comment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board', sa.Column('comment', sa.VARCHAR(length=300), server_default=sa.text("'1'::character varying"), autoincrement=False, nullable=False))
    op.drop_column('board', 'content')
    # ### end Alembic commands ###