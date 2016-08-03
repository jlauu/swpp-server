"""empty message

Revision ID: 411dba076aec
Revises: 8b7c5da245e5
Create Date: 2016-08-03 09:54:56.499896

"""

# revision identifiers, used by Alembic.
revision = '411dba076aec'
down_revision = '8b7c5da245e5'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cluster_hierarchy', sa.Column('data', postgresql.JSON(), nullable=False))
    op.drop_constraint('cluster_hierarchy_parent_key', 'cluster_hierarchy', type_='unique')
    op.drop_column('cluster_hierarchy', 'children')
    op.drop_column('cluster_hierarchy', 'parent')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cluster_hierarchy', sa.Column('parent', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('cluster_hierarchy', sa.Column('children', postgresql.ARRAY(INTEGER()), autoincrement=False, nullable=True))
    op.create_unique_constraint('cluster_hierarchy_parent_key', 'cluster_hierarchy', ['parent'])
    op.drop_column('cluster_hierarchy', 'data')
    ### end Alembic commands ###