"""create users table

Revision ID: f00e24afdea7
Revises: 
Create Date: 2025-09-19 00:30:42.778241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f00e24afdea7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create gender enum
    gender_enum = sa.Enum("MALE", "FEMALE", "OTHERS", name="genderenum", create_type=False)

    # Create role enum
    role_enum = sa.Enum("ADMIN", "USER", name="roleenum", create_type=False)

    # Create users table
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer, primary_key=True, index=True, autoincrement=True),
        sa.Column("first_name", sa.String(50), nullable=False),
        sa.Column("last_name", sa.String(50), nullable=False),
        sa.Column("gender", gender_enum, nullable=False),
        sa.Column("email", sa.String(100), unique=True, nullable=False, index=True),
        sa.Column("phone_number", sa.String(10), nullable=False),
        sa.Column("role", role_enum, nullable=False, server_default="USER"),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS genderenum")
    op.execute("DROP TYPE IF EXISTS roleenum")
