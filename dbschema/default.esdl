
module default {
  type Chat {
    required property chat_id -> int64{constraint exclusive;};
    required property title -> str;
  }

  scalar type GameStatus extending enum<Enrollment, Ended>;
  type Game {
    required property status -> GameStatus;
    required property start_date -> datetime{default:= datetime_current()};

    required link chat -> Chat{on target delete delete source;};
  }

  scalar type PlayerRole extending enum<Civilian, Mafia>;
  type Player {
    required property user_id -> int64{constraint exclusive;};
    required property name -> str;
    required property role -> PlayerRole{default:= PlayerRole.Civilian};

    required link game -> Game{on target delete delete source;};
    required link chat -> Chat{on target delete delete source;};
  }

  scalar type MessagePayload extending enum<Enrollment, Timer>;
  type Message {
    required property message_id -> int64;
    required property message_payload -> MessagePayload;

    required link game -> Game{on target delete delete source;};
    required link chat -> Chat{on target delete delete source;};
  }
}
