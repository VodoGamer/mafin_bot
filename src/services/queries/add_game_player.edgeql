select (
  insert Player {
    user_id := <int64>$user_id,
    name := <str>$name,
    chat := (
      select Chat filter .chat_id=<int64>$chat_id
    ),
    game := (
      select Game filter .id=<uuid>$game_id
    )
  }
) {**};
