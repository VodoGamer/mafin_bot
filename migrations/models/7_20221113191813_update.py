from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "game_message" ADD "chat_id" BIGINT;
        ALTER TABLE "game_message" ALTER COLUMN "payload" TYPE SMALLINT USING "payload"::SMALLINT;
        CREATE TABLE IF NOT EXISTS "night" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "start_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "game_message" DROP COLUMN "chat_id";
        ALTER TABLE "game_message" ALTER COLUMN "payload" TYPE SMALLINT USING "payload"::SMALLINT;
        DROP TABLE IF EXISTS "night";"""
