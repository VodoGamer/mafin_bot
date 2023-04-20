select Message {**} filter Message.chat.chat_id = <int64>$chat_id and Message.message_payload = <MessagePayload>$message_payload;
