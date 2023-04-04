"""Add MR_Member_Tag table

Revision ID: 84523463fe09
Revises: 8c5bdd75dd78
Create Date: 2023-04-04 01:53:26.957824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84523463fe09'
down_revision = '8c5bdd75dd78'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('MR_Member_Tag',
    sa.Column('member_uuid', sa.UUID(), nullable=False),
    sa.Column('tag_text', sa.String(), nullable=False),
    sa.Column('is_self_tag', sa.Boolean(), nullable=False),
    sa.Column('is_find_tag', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['member_uuid'], ['MR_Member.member_uuid'], ),
    sa.PrimaryKeyConstraint('member_uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('MR_Member_Tag')
    # ### end Alembic commands ###