"""jwttokens

Revision ID: 32988536753a
Revises: 57213bdc65ee
Create Date: 2020-11-30 19:06:14.182778

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32988536753a'
down_revision = '57213bdc65ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blacklist_tokens',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('blacklisted_on', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blacklist_tokens')
    # ### end Alembic commands ###