"""Add local credentials, admin roles, and security audit event storage."""

from alembic import op
import sqlalchemy as sa


revision = "0002_local_auth_rbac"
down_revision = "0001_create_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create authentication tables, seed the admin role, and index audit time."""
    op.create_table(
        "auth_roles",
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint("name"),
    )
    op.bulk_insert(
        sa.table("auth_roles", sa.column("name", sa.String(length=64))),
        [{"name": "admin"}],
    )
    op.create_table(
        "local_credentials",
        sa.Column(
            "user_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column(
            "is_enabled",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "session_version",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("user_id"),
    )
    op.create_table(
        "user_roles",
        sa.Column(
            "user_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "role_name",
            sa.String(length=64),
            sa.ForeignKey("auth_roles.name", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "assigned_by",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "assigned_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("user_id", "role_name"),
    )
    op.create_table(
        "security_audit_events",
        sa.Column("id", sa.Uuid(as_uuid=True), nullable=False),
        sa.Column(
            "actor_user_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "target_user_id",
            sa.Uuid(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("source_ip", sa.String(length=64), nullable=True),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_security_audit_events_occurred_at",
        "security_audit_events",
        ["occurred_at"],
    )


def downgrade() -> None:
    """Drop authentication tables and their audit index in dependency order."""
    op.drop_index("ix_security_audit_events_occurred_at", table_name="security_audit_events")
    op.drop_table("security_audit_events")
    op.drop_table("user_roles")
    op.drop_table("local_credentials")
    op.drop_table("auth_roles")
