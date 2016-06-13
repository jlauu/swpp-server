"""empty message

Revision ID: 501c197c6f37
Revises: fb01026f520b
Create Date: 2016-06-13 17:05:47.515871

"""

# revision identifiers, used by Alembic.
revision = '501c197c6f37'
down_revision = 'fb01026f520b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('interactions',
    sa.PrimaryKeyConstraint('id'),
    sa.Column('userid', sa.String(), nullable=True),
    sa.Column('event', sa.String(), nullable=True),
    sa.Column('windowid', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('time', sa.BigInteger(), nullable=True),
    )
    pass


def downgrade():
    op.drop_table('interactions')
    pass
