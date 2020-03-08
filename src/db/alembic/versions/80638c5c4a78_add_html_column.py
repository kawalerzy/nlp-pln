"""add html column

Revision ID: 80638c5c4a78
Revises: 6cc3fb1ccd30
Create Date: 2020-03-06 23:34:42.115230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80638c5c4a78'
down_revision = '6cc3fb1ccd30'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pilkanoznapl', sa.Column('html', sa.TEXT(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pilkanoznapl', 'html')
    # ### end Alembic commands ###