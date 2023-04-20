
module default {
  type Chat {
    required property chat_id -> int64{constraint exclusive;};
    required property title -> str;
  }

  scalar type GameStatus extending enum<Enrollment, Ended>;
  type Game {
    required property status -> GameStatus;
    required property start_date -> datetime{default:= datetime_current()};

    required link chat -> Chat;
  }

  type Player {
    required property user_id -> int64{constraint exclusive;};
    required property name -> str;

    required link game -> Game;
    required link chat -> Chat;
  }

  scalar type MessagePayload extending enum<Enrollment>;
  type Message {
    required property message_id -> int64;
    required property message_payload -> MessagePayload;

    required link game -> Game;
    required link chat -> Chat;
  }
}
