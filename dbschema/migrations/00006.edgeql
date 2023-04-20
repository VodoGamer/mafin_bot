CREATE MIGRATION m1trknkzrrwtsobhnxo3yhcupmrploa63u3lnxbpyzszqcttvm6mgq
    ONTO m1vhjbw6jmpnjxevwivg7h7kwnqaxs2maf272dge3hirq7gx6vxxia
{
  CREATE SCALAR TYPE default::MessagePayload EXTENDING enum<Enrollment>;
  CREATE TYPE default::Message {
      CREATE REQUIRED LINK chat: default::Chat;
      CREATE REQUIRED LINK game: default::Game;
      CREATE REQUIRED PROPERTY message_id: std::int64;
      CREATE REQUIRED PROPERTY message_payload: default::MessagePayload;
  };
};
