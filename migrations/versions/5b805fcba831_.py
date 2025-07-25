"""empty message

Revision ID: 5b805fcba831
Revises: b85236abd26c
Create Date: 2025-06-29 14:31:39.256306

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5b805fcba831'
down_revision = 'b85236abd26c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_verifications', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('verification_code',
               existing_type=sa.VARCHAR(length=6),
               nullable=False)
        batch_op.alter_column('code_expiration',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
        batch_op.drop_constraint(batch_op.f('user_verifications_user_id_key'), type_='unique')
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_verifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
        batch_op.create_unique_constraint(batch_op.f('user_verifications_user_id_key'), ['user_id'])
        batch_op.alter_column('code_expiration',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
        batch_op.alter_column('verification_code',
               existing_type=sa.VARCHAR(length=6),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
