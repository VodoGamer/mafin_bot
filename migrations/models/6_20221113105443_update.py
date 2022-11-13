from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "player" ADD "life" SMALLINT NOT NULL  DEFAULT 1;
        ALTER TABLE "player" ALTER COLUMN "role" TYPE VARCHAR(13) USING "role"::VARCHAR(13);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "player" DROP COLUMN "life";
        ALTER TABLE "player" ALTER COLUMN "role" TYPE VARCHAR(13) USING "role"::VARCHAR(13);"""
