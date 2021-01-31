"""empty message

Revision ID: 1835acfe8d82
Revises: 8fc230e4b757
Create Date: 2021-01-31 12:18:42.126478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1835acfe8d82'
down_revision = '8fc230e4b757'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todo_list', sa.Column('completed', sa.Boolean(), nullable=True))

    op.execute('UPDATE todo_list SET completed = False WHERE completed IS NULL;')

    op.alter_column('todo_list','completed', nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todo_list', 'completed')
    # ### end Alembic commands ###
