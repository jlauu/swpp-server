"""empty message

Revision ID: fb01026f520b
Revises: 3ff4cf5c5df3
Create Date: 2016-06-10 14:57:30.610033

"""

# revision identifiers, used by Alembic.
revision = 'fb01026f520b'
down_revision = '3ff4cf5c5df3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('ALTER TABLE linkclicks ALTER COLUMN time TYPE BIGINT')
    pass


def downgrade():
    op.execute('ALTER TABLE linkclicks ALTER COLUMN time TYPE INTEGER')
    pass
