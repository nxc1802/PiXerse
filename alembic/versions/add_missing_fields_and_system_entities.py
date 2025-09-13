"""Add missing fields and system entities

Revision ID: add_missing_fields
Revises: c5ca601b6846
Create Date: 2025-01-27 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_missing_fields'
down_revision: Union[str, None] = 'c5ca601b6846'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Update existing tables with new fields
    
    # Update members table
    op.add_column('members', sa.Column('member_name', sa.String(length=255), nullable=False, server_default='Unknown'))
    op.add_column('members', sa.Column('avatar_url', sa.String(length=500), nullable=True))
    op.alter_column('members', 'project_id', nullable=True)
    
    # Update blogs table
    op.add_column('blogs', sa.Column('author_id', sa.Integer(), nullable=False, server_default='1'))
    op.add_column('blogs', sa.Column('category', sa.String(length=50), nullable=True))
    op.add_column('blogs', sa.Column('tags', sa.JSON(), nullable=True))
    op.add_column('blogs', sa.Column('featured_image', sa.String(length=500), nullable=True))
    op.alter_column('blogs', 'project_id', nullable=True)
    op.alter_column('blogs', 'title', type_=sa.String(length=500))
    op.alter_column('blogs', 'detail', new_column_name='content')
    
    # Update assets table
    op.add_column('assets', sa.Column('youtube_video_id', sa.String(length=100), nullable=True))
    op.add_column('assets', sa.Column('description', sa.Text(), nullable=True))
    op.alter_column('assets', 'original_filename', nullable=True)
    op.alter_column('assets', 'cloudinary_public_id', nullable=True)
    op.alter_column('assets', 'cloudinary_url', nullable=True)
    op.alter_column('assets', 'file_size', type_=sa.BigInteger(), server_default='0')
    op.alter_column('assets', 'mime_type', nullable=True)
    op.drop_column('assets', 'cloudinary_secure_url')
    
    # Update asset_type enum
    op.execute("ALTER TYPE assettype RENAME TO assettype_old")
    op.execute("CREATE TYPE assettype AS ENUM ('IMAGE', 'VIDEO', 'YOUTUBE')")
    op.execute("ALTER TABLE assets ALTER COLUMN asset_type TYPE assettype USING asset_type::text::assettype")
    op.execute("DROP TYPE assettype_old")
    
    # Create admin_users table
    op.create_table('admin_users',
        sa.Column('admin_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('admin_id')
    )
    op.create_index(op.f('ix_admin_users_admin_id'), 'admin_users', ['admin_id'], unique=False)
    op.create_index(op.f('ix_admin_users_username'), 'admin_users', ['username'], unique=True)
    
    # Create admin_sessions table
    op.create_table('admin_sessions',
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('admin_id', sa.Integer(), nullable=False),
        sa.Column('session_token', sa.String(length=255), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['admin_id'], ['admin_users.admin_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('session_id')
    )
    op.create_index(op.f('ix_admin_sessions_session_id'), 'admin_sessions', ['session_id'], unique=False)
    op.create_index(op.f('ix_admin_sessions_session_token'), 'admin_sessions', ['session_token'], unique=True)
    
    # Create chat_sessions table
    op.create_table('chat_sessions',
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('session_token', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('last_activity_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('session_id')
    )
    op.create_index(op.f('ix_chat_sessions_session_id'), 'chat_sessions', ['session_id'], unique=False)
    op.create_index(op.f('ix_chat_sessions_session_token'), 'chat_sessions', ['session_token'], unique=True)
    
    # Create chat_messages table
    op.create_table('chat_messages',
        sa.Column('message_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.Enum('USER', 'ASSISTANT', name='messagerole'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['chat_sessions.session_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('message_id')
    )
    op.create_index(op.f('ix_chat_messages_message_id'), 'chat_messages', ['message_id'], unique=False)
    
    # Create tool_calls table
    op.create_table('tool_calls',
        sa.Column('tool_call_id', sa.Integer(), nullable=False),
        sa.Column('message_id', sa.Integer(), nullable=False),
        sa.Column('tool_name', sa.String(length=100), nullable=False),
        sa.Column('tool_input', sa.JSON(), nullable=True),
        sa.Column('tool_output', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['message_id'], ['chat_messages.message_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('tool_call_id')
    )
    op.create_index(op.f('ix_tool_calls_tool_call_id'), 'tool_calls', ['tool_call_id'], unique=False)
    
    # Add foreign key constraints
    op.create_foreign_key('fk_blogs_author_id', 'blogs', 'members', ['author_id'], ['member_id'], ondelete='CASCADE')


def downgrade() -> None:
    # Drop foreign key constraints
    op.drop_constraint('fk_blogs_author_id', 'blogs', type_='foreignkey')
    
    # Drop new tables
    op.drop_table('tool_calls')
    op.drop_table('chat_messages')
    op.drop_table('chat_sessions')
    op.drop_table('admin_sessions')
    op.drop_table('admin_users')
    
    # Revert asset_type enum
    op.execute("ALTER TYPE assettype RENAME TO assettype_old")
    op.execute("CREATE TYPE assettype AS ENUM ('image', 'video', 'document', 'other')")
    op.execute("ALTER TABLE assets ALTER COLUMN asset_type TYPE assettype USING asset_type::text::assettype")
    op.execute("DROP TYPE assettype_old")
    
    # Revert assets table changes
    op.add_column('assets', sa.Column('cloudinary_secure_url', sa.Text(), nullable=False, server_default=''))
    op.alter_column('assets', 'mime_type', nullable=False)
    op.alter_column('assets', 'file_size', type_=sa.Integer(), server_default=None)
    op.alter_column('assets', 'cloudinary_url', nullable=False)
    op.alter_column('assets', 'cloudinary_public_id', nullable=False)
    op.alter_column('assets', 'original_filename', nullable=False)
    op.drop_column('assets', 'description')
    op.drop_column('assets', 'youtube_video_id')
    
    # Revert blogs table changes
    op.alter_column('blogs', 'content', new_column_name='detail')
    op.alter_column('blogs', 'title', type_=sa.Text())
    op.alter_column('blogs', 'project_id', nullable=False)
    op.drop_column('blogs', 'featured_image')
    op.drop_column('blogs', 'tags')
    op.drop_column('blogs', 'category')
    op.drop_column('blogs', 'author_id')
    
    # Revert members table changes
    op.alter_column('members', 'project_id', nullable=False)
    op.drop_column('members', 'avatar_url')
    op.drop_column('members', 'member_name')
