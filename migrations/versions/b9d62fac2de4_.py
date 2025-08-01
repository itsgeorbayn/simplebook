"""empty message

Revision ID: b9d62fac2de4
Revises: d2224ec31ff4
Create Date: 2025-07-10 19:15:12.093001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9d62fac2de4'
down_revision = 'd2224ec31ff4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_banned', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('banned_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('banned_at')
        batch_op.drop_column('is_banned')

    # ### end Alembic commands ###
