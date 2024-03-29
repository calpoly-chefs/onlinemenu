"""add remixes as adjacency list

Revision ID: 5f2f0497a5c2
Revises: 7f94bebbaa9f
Create Date: 2019-09-29 09:26:00.280192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f2f0497a5c2'
down_revision = '7f94bebbaa9f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.add_column(sa.Column('parent_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_recipe_parent_id_recipe'), 'recipe', ['parent_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('recipe', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_recipe_parent_id_recipe'), type_='foreignkey')
        batch_op.drop_column('parent_id')

    # ### end Alembic commands ###
