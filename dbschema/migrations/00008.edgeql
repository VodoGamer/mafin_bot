CREATE MIGRATION m1jm2qj3fnixrdn5qv7lcfgljb3taxbiy6o7uhf3xlykxbf7qve3ga
    ONTO m1lnviymkresjhf2xv7tggfai4b743uqdp3ppwbv57nnzqadopnnuq
{
  ALTER TYPE default::Game {
      ALTER LINK chat {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE default::Game {
      ALTER PROPERTY game_start_date {
          RENAME TO start_date;
      };
  };
  ALTER TYPE default::Game {
      ALTER PROPERTY game_status {
          RENAME TO status;
      };
  };
  ALTER TYPE default::Message {
      ALTER LINK chat {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE default::Message {
      ALTER LINK game {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE default::Player {
      ALTER LINK chat {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE default::Player {
      ALTER LINK game {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
};
