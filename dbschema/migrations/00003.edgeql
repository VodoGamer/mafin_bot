CREATE MIGRATION m1udor46kkyktgee4nlhvn3z5torgkzspcft2rgis542bbi72jtnba
    ONTO m1afrg7qcofdkkqvuvlgx4kimlmftw3uovtxyx63bhhujmp4z5p6wq
{
  CREATE SCALAR TYPE default::GameStatus EXTENDING enum<Enrollment, Ended>;
  ALTER TYPE default::Game {
      CREATE REQUIRED PROPERTY game_status: default::GameStatus {
          SET REQUIRED USING ('Ended');
      };
  };
};
