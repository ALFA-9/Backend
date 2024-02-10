"""First migration

Revision ID: 632fc967fc35
Revises: 
Create Date: 2024-02-10 05:17:52.225480

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "632fc967fc35"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum("in_work", "not_completed", "done", "cancelled", name="statusidp").create(
        op.get_bind()
    )
    sa.Enum(
        "in_work", "done", "not_completed", "cancelled", name="statusprogress"
    ).create(op.get_bind())
    op.create_table(
        "control",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "department",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "grade",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "post",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "type",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "employee",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("grade_id", sa.Integer(), nullable=True),
        sa.Column("post_id", sa.Integer(), nullable=True),
        sa.Column("department_id", sa.Integer(), nullable=True),
        sa.Column("director_id", sa.Integer(), nullable=True),
        sa.Column("first_name", sa.String(length=80), nullable=True),
        sa.Column("last_name", sa.String(length=80), nullable=True),
        sa.Column("patronymic", sa.String(length=80), nullable=True),
        sa.Column("email", sa.String(length=100), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(
            ["department_id"], ["department.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["director_id"], ["employee.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["grade_id"], ["grade.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["post_id"], ["post.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "idp",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=True),
        sa.Column("employee_id", sa.Integer(), nullable=True),
        sa.Column("director_id", sa.Integer(), nullable=True),
        sa.Column(
            "status_idp",
            postgresql.ENUM(
                "in_work",
                "not_completed",
                "done",
                "cancelled",
                name="statusidp",
                create_type=False,
            ),
            nullable=True,
        ),
        sa.Column(
            "date_start",
            sa.Date(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("date_end", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(
            ["director_id"],
            ["employee.id"],
        ),
        sa.ForeignKeyConstraint(["employee_id"], ["employee.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("idp_id", sa.Integer(), nullable=True),
        sa.Column(
            "status_progress",
            postgresql.ENUM(
                "in_work",
                "done",
                "not_completed",
                "cancelled",
                name="statusprogress",
                create_type=False,
            ),
            nullable=True,
        ),
        sa.Column("is_completed", sa.Boolean(), nullable=True),
        sa.Column("date_start", sa.Date(), nullable=True),
        sa.Column("date_end", sa.Date(), nullable=True),
        sa.Column("type_id", sa.Integer(), nullable=True),
        sa.Column("control_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["control_id"], ["control.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["idp_id"], ["idp.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["type_id"], ["type.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "comment",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("body_comment", sa.String(length=200), nullable=True),
        sa.Column("task_id", sa.Integer(), nullable=True),
        sa.Column("employee_id", sa.Integer(), nullable=True),
        sa.Column(
            "pub_date",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["employee_id"], ["employee.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["task_id"], ["task.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("comment")
    op.drop_table("task")
    op.drop_table("idp")
    op.drop_table("employee")
    op.drop_table("type")
    op.drop_table("post")
    op.drop_table("grade")
    op.drop_table("department")
    op.drop_table("control")
    sa.Enum("in_work", "done", "not_completed", "cancelled", name="statusprogress").drop(
        op.get_bind()
    )
    sa.Enum("in_work", "not_completed", "done", "cancelled", name="statusidp").drop(
        op.get_bind()
    )
    # ### end Alembic commands ###
