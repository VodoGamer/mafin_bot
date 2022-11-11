from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "player" ALTER COLUMN "role" SET DEFAULT 'Role.civilian';
        ALTER TABLE "player" ALTER COLUMN "role" SET NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "player" ALTER COLUMN "role" DROP NOT NULL;
        ALTER TABLE "player" ALTER COLUMN "role" DROP DEFAULT;"""
