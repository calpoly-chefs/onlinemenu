"""add user info

Revision ID: fe7d4cd37fda
Revises: ef6cc29c66e7
Create Date: 2019-10-06 16:14:33.141365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe7d4cd37fda'
down_revision = 'ef6cc29c66e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_following',
    sa.Column('user_username', sa.String(length=50), nullable=False),
    sa.Column('following_username', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['following_username'], ['user.username'], name=op.f('fk_user_following_following_username_user')),
    sa.ForeignKeyConstraint(['user_username'], ['user.username'], name=op.f('fk_user_following_user_username_user')),
    sa.PrimaryKeyConstraint('user_username', 'following_username', name=op.f('pk_user_following'))
    )
    op.create_table('likes',
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.id'], name=op.f('fk_likes_recipe_id_recipe')),
    sa.ForeignKeyConstraint(['username'], ['user.username'], name=op.f('fk_likes_username_user'))
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('badges', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('bio', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('bio')
        batch_op.drop_column('badges')

    op.drop_table('likes')
    op.drop_table('user_following')
    # ### end Alembic commands ###
