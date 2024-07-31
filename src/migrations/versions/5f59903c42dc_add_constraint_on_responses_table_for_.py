"""Add constraint on responses table for user amd job fields

Revision ID: 5f59903c42dc
Revises: 2e444e7e86e1
Create Date: 2024-08-01 01:16:26.271058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f59903c42dc'
down_revision = '2e444e7e86e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'jobs', ['id'])
    op.create_unique_constraint('uix_user_job', 'responses', ['user_id', 'job_id'])
    op.create_unique_constraint(None, 'responses', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'responses', type_='unique')
    op.drop_constraint('uix_user_job', 'responses', type_='unique')
    op.drop_constraint(None, 'jobs', type_='unique')
    # ### end Alembic commands ###