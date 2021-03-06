"""empty message

Revision ID: 9abce378b63a
Revises: ee0585848c1a
Create Date: 2021-02-21 12:19:57.120758

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9abce378b63a'
down_revision = 'ee0585848c1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board', sa.Column('content', sa.String(length=300), nullable=True))
    op.drop_column('board', 'comment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('board', sa.Column('comment', sa.VARCHAR(length=300), server_default=sa.text("'1'::character varying"), autoincrement=False, nullable=False))
    op.drop_column('board', 'content')
    # ### end Alembic commands ###
