CREATE MIGRATION m1vhjbw6jmpnjxevwivg7h7kwnqaxs2maf272dge3hirq7gx6vxxia
    ONTO m1b2zzjuj7inz2lzoaascyddp2ugmutkhs36sygo4shuskwksz7e5q
{
  ALTER TYPE default::Game {
      ALTER PROPERTY game_status {
          DROP CONSTRAINT std::exclusive;
      };
  };
};
