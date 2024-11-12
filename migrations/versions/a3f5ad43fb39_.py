"""empty message

Revision ID: a3f5ad43fb39
Revises: fb269825c351
Create Date: 2024-11-07 23:21:39.049501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3f5ad43fb39'
down_revision = 'fb269825c351'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('goal_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(None, 'goal', ['goal_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('goal_id')

    # ### end Alembic commands ###