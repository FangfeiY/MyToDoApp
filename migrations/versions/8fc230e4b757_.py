"""empty message

Revision ID: 8fc230e4b757
Revises: b2a479e69d35
Create Date: 2021-01-24 13:56:03.812375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fc230e4b757'
down_revision = 'b2a479e69d35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    todo_list = op.create_table('todo_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )

    op.bulk_insert(todo_list,
        [
            {'id':1, 'name':'Uncategorized'}
        ],
    )

    op.add_column('todo_item', sa.Column('list_id', sa.Integer(), nullable=True))

    op.execute('UPDATE todo_item SET list_id = 1 WHERE list_id IS NULL;')

    op.alter_column('todo_item','list_id', nullable=False)

    op.create_foreign_key(None, 'todo_item', 'todo_list', ['list_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todo_item', type_='foreignkey')
    op.drop_column('todo_item', 'list_id')
    op.drop_table('todo_list')
    # ### end Alembic commands ###
