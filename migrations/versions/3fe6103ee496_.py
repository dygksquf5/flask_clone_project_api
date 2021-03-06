"""empty message

Revision ID: 3fe6103ee496
Revises: df83d473d194
Create Date: 2021-02-25 15:26:18.809348

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3fe6103ee496'
down_revision = 'df83d473d194'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('option_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'cart', 'option', ['option_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cart', type_='foreignkey')
    op.drop_column('cart', 'option_id')
    # ### end Alembic commands ###
