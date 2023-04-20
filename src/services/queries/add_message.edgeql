select (
  insert Message {
    message_id := <int64>$message_id,
    message_payload := <str>$message_payload,
    chat := (
      select Chat filter .chat_id=<int64>$chat_id
    ),
    game := (
      select Game filter .id=<uuid>$game_uuid
    )
  }
) {**};
