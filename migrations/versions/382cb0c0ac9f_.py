"""empty message

Revision ID: 382cb0c0ac9f
Revises: 1c7003672877
Create Date: 2025-07-03 19:05:13.207182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '382cb0c0ac9f'
down_revision = '1c7003672877'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin_permissions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('list_admins', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('edit_admins', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin_permissions', schema=None) as batch_op:
        batch_op.drop_column('edit_admins')
        batch_op.drop_column('list_admins')

    # ### end Alembic commands ###
