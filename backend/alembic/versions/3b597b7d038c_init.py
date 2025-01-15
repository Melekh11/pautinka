"""Init

Revision ID: 3b597b7d038c
Revises: 
Create Date: 2025-01-15 19:13:24.382219

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = "3b597b7d038c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("surname", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("last_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("phone", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("university", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("birthdate", sa.Date(), nullable=True),
        sa.Column("course", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("short_status", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("full_status", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("about_me", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("links", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "subscription",
        sa.Column("user_id_from", sa.Integer(), nullable=False),
        sa.Column("user_id_to", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id_from"],
            ["users.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id_to"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id_from", "user_id_to"),
    )
    op.create_table(
        "tagsusers",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tag_id"],
            ["tags.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "tag_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tagsusers")
    op.drop_table("subscription")
    op.drop_table("users")
    op.drop_table("tags")
    # ### end Alembic commands ###
