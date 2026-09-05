"""create_initial_tables

Revision ID: a5c4ac96cf10
Revises: 
Create Date: 2026-09-05 19:42:31.870294
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5c4ac96cf10'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. Create sections table ─────────────────────────────────────────
    op.create_table(
        'sections',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('section_code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('route_from', sa.String(length=100), nullable=False),
        sa.Column('route_to', sa.String(length=100), nullable=False),
        sa.Column('km_start', sa.Float(), nullable=False),
        sa.Column('km_end', sa.Float(), nullable=False),
        sa.Column('status', sa.String(length=50), server_default='ACTIVE', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_sections_section_code', 'sections', ['section_code'], unique=True)

    # ── 2. Create maintenance_tasks table ─────────────────────────────
    op.create_table(
        'maintenance_tasks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('section_id', sa.Integer(), nullable=False),
        sa.Column('department', sa.Enum('ENGINEERING', 'ELECTRICAL', 'SIGNAL', name='department_enum', native_enum=False), nullable=False),
        sa.Column('task_type', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('duration_minutes', sa.Integer(), nullable=False),
        sa.Column('criticality', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('urgency', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('overdue_days', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('safety_impact', sa.Enum('LOW', 'MEDIUM', 'HIGH', name='safety_enum', native_enum=False), nullable=False),
        sa.Column('required_resources', sa.JSON(), nullable=True),
        sa.Column('preferred_start_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('preferred_end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deadline', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'PRIORITIZED', 'SCHEDULED', 'COMPLETED', 'CANCELLED', name='taskstatus_enum', native_enum=False), nullable=False, server_default='PENDING'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_maintenance_tasks_section_id', 'maintenance_tasks', ['section_id'], unique=False)
    op.create_index('ix_maintenance_tasks_department', 'maintenance_tasks', ['department'], unique=False)
    op.create_index('ix_maintenance_tasks_status', 'maintenance_tasks', ['status'], unique=False)
    op.create_index('ix_maintenance_tasks_deadline', 'maintenance_tasks', ['deadline'], unique=False)

    # ── 3. Create train_schedules table ──────────────────────────────
    op.create_table(
        'train_schedules',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('train_number', sa.String(length=50), nullable=False),
        sa.Column('train_name', sa.String(length=100), nullable=False),
        sa.Column('train_type', sa.Enum('EXPRESS', 'PASSENGER', 'GOODS', 'SPECIAL', name='traintype_enum', native_enum=False), nullable=False),
        sa.Column('section_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('arrival_time', sa.Time(), nullable=False),
        sa.Column('departure_time', sa.Time(), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_train_schedules_train_number', 'train_schedules', ['train_number'], unique=False)
    op.create_index('ix_train_schedules_section_id', 'train_schedules', ['section_id'], unique=False)
    op.create_index('ix_train_schedules_date', 'train_schedules', ['date'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_train_schedules_date', table_name='train_schedules')
    op.drop_index('ix_train_schedules_section_id', table_name='train_schedules')
    op.drop_index('ix_train_schedules_train_number', table_name='train_schedules')
    op.drop_table('train_schedules')

    op.drop_index('ix_maintenance_tasks_deadline', table_name='maintenance_tasks')
    op.drop_index('ix_maintenance_tasks_status', table_name='maintenance_tasks')
    op.drop_index('ix_maintenance_tasks_department', table_name='maintenance_tasks')
    op.drop_index('ix_maintenance_tasks_section_id', table_name='maintenance_tasks')
    op.drop_table('maintenance_tasks')

    op.drop_index('ix_sections_section_code', table_name='sections')
    op.drop_table('sections')
