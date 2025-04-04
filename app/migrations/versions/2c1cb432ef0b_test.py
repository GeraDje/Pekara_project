"""test

Revision ID: 2c1cb432ef0b
Revises: 611806752261
Create Date: 2025-04-02 13:00:03.338585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c1cb432ef0b'
down_revision: Union[str, None] = '611806752261'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receipts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('total_amount', sa.Integer(), nullable=False),
    sa.Column('received_amount', sa.Integer(), nullable=True),
    sa.Column('change', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('receipt_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('receipt_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['receipt_id'], ['receipts.id'], ),
    sa.PrimaryKeyConstraint('id', 'receipt_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('receipt_items')
    op.drop_table('receipts')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('products')
    # ### end Alembic commands ###
