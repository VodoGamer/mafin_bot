CREATE MIGRATION m13hxh4bxazl4rfogadwevswrbeep7iu527wm535slmselk6g2ed6a
    ONTO m1723t4cwptr5t3k5dgqsgmlnytbyos6am4idp3gcfegdlvrnp4cwq
{
  CREATE SCALAR TYPE default::PlayerRole EXTENDING enum<Civilian, Mafia>;
  ALTER TYPE default::Player {
      CREATE REQUIRED PROPERTY role: default::PlayerRole {
          SET default := (default::PlayerRole.Civilian);
      };
  };
};
