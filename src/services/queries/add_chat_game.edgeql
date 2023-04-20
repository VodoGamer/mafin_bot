select (
  insert Game {
    chat := (
      insert Chat{
        chat_id := <int64>$chat_id,
        title := <str>$title
      }
      unless conflict on .chat_id
      else (
        select Chat filter .chat_id=<int64>$chat_id
      )
    ),
    status := <str>'Enrollment'
  }
) {**};
