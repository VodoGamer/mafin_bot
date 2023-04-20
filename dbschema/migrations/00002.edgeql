CREATE MIGRATION m1afrg7qcofdkkqvuvlgx4kimlmftw3uovtxyx63bhhujmp4z5p6wq
    ONTO m1bp4ncokm53ivbh4qakox3wtmbfhcd3euwejnql77f5purjejlsqq
{
  CREATE TYPE default::Player {
      CREATE REQUIRED LINK chat: default::Chat;
      CREATE REQUIRED LINK game: default::Game;
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE REQUIRED PROPERTY user_id: std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
