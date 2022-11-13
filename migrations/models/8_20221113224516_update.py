from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "day" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "start_date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE
);;
        ALTER TABLE "game_message" ALTER COLUMN "payload" TYPE SMALLINT USING "payload"::SMALLINT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "game_message" ALTER COLUMN "payload" TYPE SMALLINT USING "payload"::SMALLINT;
        DROP TABLE IF EXISTS "day";"""
