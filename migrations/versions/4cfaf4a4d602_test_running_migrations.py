"""test running migrations

Revision ID: 4cfaf4a4d602
Revises: c44d4abd3656
Create Date: 2024-01-18 02:16:00.127390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4cfaf4a4d602'
down_revision: Union[str, None] = 'c44d4abd3656'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
