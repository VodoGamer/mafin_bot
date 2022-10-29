from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "player" RENAME COLUMN "username" TO "name";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "player" RENAME COLUMN "name" TO "username";"""
