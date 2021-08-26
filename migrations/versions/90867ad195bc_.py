"""empty message

Revision ID: 90867ad195bc
Revises: e1e6242ede97
Create Date: 2021-08-24 04:23:21.938773

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '90867ad195bc'
down_revision = 'e1e6242ede97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('character', sa.Column('weight', sa.String(length=50), nullable=False))
    op.drop_column('character', 'weitght')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('character', sa.Column('weitght', mysql.VARCHAR(length=50), nullable=False))
    op.drop_column('character', 'weight')
    # ### end Alembic commands ###