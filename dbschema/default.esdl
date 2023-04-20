
module default {
  type Chat {
    required property chat_id -> int64{constraint exclusive;};
    required property title -> str;
  }

  scalar type GameStatus extending enum<Enrollment, Ended>;
  type Game {
    required property game_status -> GameStatus;

    required link chat -> Chat;
  }

  type Player {
    required property user_id -> int64{constraint exclusive;};
    required property name -> str;

    required link game -> Game;
    required link chat -> Chat;
  }
}
