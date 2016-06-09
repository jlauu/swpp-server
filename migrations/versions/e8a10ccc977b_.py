"""empty message

Revision ID: e8a10ccc977b
Revises: 6103a4e20c07
Create Date: 2016-06-09 10:58:17.335063

"""

# revision identifiers, used by Alembic.
revision = 'e8a10ccc977b'
down_revision = '6103a4e20c07'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('ALTER TABLE pagevisits ALTER COLUMN sessionid TYPE varchar(30)')
    pass


def downgrade():
    op.execute('ALTER TABLE pagevisits ALTER COLUMN sessionid TYPE INTEGER')
    pass
