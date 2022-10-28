from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "game_action" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "type" SMALLINT NOT NULL,
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE,
    "player_id" BIGINT NOT NULL REFERENCES "player" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "game_action"."type" IS 'kill: 0\nrevived: 1';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "game_action";"""
