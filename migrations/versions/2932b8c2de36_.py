"""empty message

Revision ID: 2932b8c2de36
Revises: 
Create Date: 2017-03-12 21:39:34.262366

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import ArrowType

# revision identifiers, used by Alembic.
revision = '2932b8c2de36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contact_messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender', sa.String(length=80), nullable=True),
    sa.Column('reach_at', sa.String(length=80), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('send_date', ArrowType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author', sa.String(length=80), nullable=True),
    sa.Column('title', sa.String(length=80), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('publish_date', ArrowType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts')
    op.drop_table('contact_messages')
    # ### end Alembic commands ###