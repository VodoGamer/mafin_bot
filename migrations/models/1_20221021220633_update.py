from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chat" DROP COLUMN "state";
        ALTER TABLE "game" ALTER COLUMN "state" TYPE SMALLINT USING "state"::SMALLINT;
        ALTER TABLE "user" ALTER COLUMN "role" TYPE VARCHAR(13) USING "role"::VARCHAR(13);
        ALTER TABLE "user" ALTER COLUMN "role" TYPE VARCHAR(13) USING "role"::VARCHAR(13);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chat" ADD "state" SMALLINT;
        ALTER TABLE "game" ALTER COLUMN "state" TYPE SMALLINT USING "state"::SMALLINT;
        ALTER TABLE "user" ALTER COLUMN "role" TYPE VARCHAR(8) USING "role"::VARCHAR(8);
        ALTER TABLE "user" ALTER COLUMN "role" TYPE VARCHAR(8) USING "role"::VARCHAR(8);"""
