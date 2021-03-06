"""ubdated album table

Revision ID: 396e24d6087f
Revises: 
Create Date: 2020-07-10 20:27:37.602298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '396e24d6087f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('album',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('album_code', sa.String(), nullable=False),
    sa.Column('artists', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('album_code')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('display_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('review',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('album_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['album_id'], ['album.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'album_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('review')
    op.drop_table('user')
    op.drop_table('album')
    # ### end Alembic commands ###
