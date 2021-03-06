"""empty message

Revision ID: 04f3c0d99441
Revises: 6e6c7cab43aa
Create Date: 2020-11-15 00:16:38.005333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04f3c0d99441'
down_revision = '6e6c7cab43aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('completed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###
    op.execute('UPDATE todos SET completed = False WHERE completed IS NULL;')

    op.alter_column('todos', 'completed', nullable=False)

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'completed')
    # ### end Alembic commands ###
