"""Renamed group->cluster

Revision ID: a8de15a59b64
Revises: ddc349e1b7a2
Create Date: 2016-06-29 10:42:09.367133

"""

# revision identifiers, used by Alembic.
revision = 'a8de15a59b64'
down_revision = 'ddc349e1b7a2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('ALTER TABLE keywords RENAME "group" TO cluster')
    pass


def downgrade():
    op.execute('ALTER TABLE keywords RENAME cluster TO "group"')
    pass
