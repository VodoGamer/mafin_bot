from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "game_action" ALTER COLUMN "type" TYPE VARCHAR(9) USING "type"::VARCHAR(9);
        ALTER TABLE "game_action" ALTER COLUMN "type" TYPE VARCHAR(9) USING "type"::VARCHAR(9);
        ALTER TABLE "game_action" ALTER COLUMN "type" TYPE VARCHAR(9) USING "type"::VARCHAR(9);
        ALTER TABLE "game_action" ALTER COLUMN "type" TYPE VARCHAR(9) USING "type"::VARCHAR(9);
        ALTER TABLE "game_action" ALTER COLUMN "type" TYPE VARCHAR(9) USING "type"::VARCHAR(9);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "game_action" ALTER COLUMN "type" TYPE SMALLINT USING "type"::SMALLINT;
        ALTER TABLE "game_action" ALTER COLUMN "type" TYPE SMALLINT USING "type"::SMALLINT;
        ALTER TABLE "game_action" ALTER COLUMN "type" TYPE SMALLINT USING "type"::SMALLINT;
        ALTER TABLE "game_action" ALTER COLUMN "type" TYPE SMALLINT USING "type"::SMALLINT;
        ALTER TABLE "game_action" ALTER COLUMN "type" TYPE SMALLINT USING "type"::SMALLINT;"""
