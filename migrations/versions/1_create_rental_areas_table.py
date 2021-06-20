"""Create rental areas table

Revision ID: 737388f98825
Revises: 
Create Date: 2021-06-20 16:50:14.002278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '737388f98825'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rental_areas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('is_leaf', sa.Boolean(), nullable=True),
    sa.Column('parent_area', sa.String(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_last_crawled', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rental_areas')
    # ### end Alembic commands ###
