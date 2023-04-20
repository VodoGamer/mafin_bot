CREATE MIGRATION m1bp4ncokm53ivbh4qakox3wtmbfhcd3euwejnql77f5purjejlsqq
    ONTO initial
{
  CREATE FUTURE nonrecursive_access_policies;
  CREATE TYPE default::Chat {
      CREATE REQUIRED PROPERTY chat_id -> std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY title -> std::str;
  };
  CREATE TYPE default::Game {
      CREATE REQUIRED LINK chat -> default::Chat;
  };
};
