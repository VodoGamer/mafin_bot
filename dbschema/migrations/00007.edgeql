CREATE MIGRATION m1lnviymkresjhf2xv7tggfai4b743uqdp3ppwbv57nnzqadopnnuq
    ONTO m1trknkzrrwtsobhnxo3yhcupmrploa63u3lnxbpyzszqcttvm6mgq
{
  ALTER TYPE default::Game {
      CREATE REQUIRED PROPERTY game_start_date: std::datetime {
          SET default := (std::datetime_current());
      };
  };
};
