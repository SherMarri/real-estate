"""Create rental table

Revision ID: e4c727734917
Revises: 737388f98825
Create Date: 2021-06-20 16:56:14.823432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4c727734917'
down_revision = '737388f98825'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rentals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('zameen_id', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('area_name', sa.String(), nullable=True),
    sa.Column('beds', sa.Integer(), nullable=True),
    sa.Column('bathrooms', sa.Integer(), nullable=True),
    sa.Column('sq_yards', sa.Integer(), nullable=True),
    sa.Column('link', sa.String(), nullable=True),
    sa.Column('date_added_on_zameen', sa.DateTime(), nullable=True),
    sa.Column('date_updated_on_zameen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rentals')
    # ### end Alembic commands ###