CREATE MIGRATION m1b2zzjuj7inz2lzoaascyddp2ugmutkhs36sygo4shuskwksz7e5q
    ONTO m1udor46kkyktgee4nlhvn3z5torgkzspcft2rgis542bbi72jtnba
{
  ALTER TYPE default::Game {
      ALTER PROPERTY game_status {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
