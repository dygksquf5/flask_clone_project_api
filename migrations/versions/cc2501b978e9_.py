"""empty message

Revision ID: cc2501b978e9
Revises: d2d3f590fb20
Create Date: 2021-03-05 10:44:20.309289

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cc2501b978e9'
down_revision = 'd2d3f590fb20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('refresh')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('refresh',
    sa.Column('uuid', postgresql.UUID(), autoincrement=False, nullable=False),
    sa.Column('refresh_token', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid', name='refresh_pkey'),
    sa.UniqueConstraint('uuid', name='refresh_uuid_key')
    )
    # ### end Alembic commands ###
