"""empty message

Revision ID: 6b99c6475051
Revises: eceb1dbebf43
Create Date: 2021-02-25 15:23:38.907892

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6b99c6475051'
down_revision = 'eceb1dbebf43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('option', sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False))
    op.drop_constraint('option_uuid_key', 'option', type_='unique')
    op.create_unique_constraint(None, 'option', ['id'])
    op.drop_column('option', 'uuid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('option', sa.Column('uuid', postgresql.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'option', type_='unique')
    op.create_unique_constraint('option_uuid_key', 'option', ['uuid'])
    op.drop_column('option', 'id')
    # ### end Alembic commands ###
