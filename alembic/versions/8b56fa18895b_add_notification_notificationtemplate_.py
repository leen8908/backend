"""Add Notification, NotificationTemplate table

Revision ID: 8b56fa18895b
Revises: 32add570a29f
Create Date: 2023-04-04 01:38:43.549680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b56fa18895b'
down_revision = '32add570a29f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('NotificationTemplate',
    sa.Column('template_uuid', sa.UUID(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('template_uuid')
    )
    op.create_table('Notification',
    sa.Column('notification_uuid', sa.UUID(), nullable=False),
    sa.Column('receiver_uuid', sa.UUID(), nullable=False),
    sa.Column('sender_uuid', sa.UUID(), nullable=True),
    sa.Column('send_time', sa.DateTime(timezone=True), nullable=False),
    sa.Column('template_uuid', sa.String(), nullable=False),
    sa.Column('f_string', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_uuid'], ['User.user_uuid'], ),
    sa.ForeignKeyConstraint(['sender_uuid'], ['User.user_uuid'], ),
    sa.PrimaryKeyConstraint('notification_uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Notification')
    op.drop_table('NotificationTemplate')
    # ### end Alembic commands ###