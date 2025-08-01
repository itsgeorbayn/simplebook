"""empty message

Revision ID: db0ae0fdc533
Revises: 0d46ef85fea9
Create Date: 2025-06-23 20:56:30.996183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db0ae0fdc533'
down_revision = '0d46ef85fea9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('is_forwarded', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('reference', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('forwarded_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('is_edited', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('edited_at', sa.DateTime(), nullable=True))
        batch_op.create_foreign_key(None, 'messages', ['reference'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('edited_at')
        batch_op.drop_column('is_edited')
        batch_op.drop_column('forwarded_at')
        batch_op.drop_column('reference')
        batch_op.drop_column('is_forwarded')
        batch_op.drop_column('deleted_at')

    # ### end Alembic commands ###
