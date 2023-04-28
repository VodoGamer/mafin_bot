CREATE MIGRATION m1723t4cwptr5t3k5dgqsgmlnytbyos6am4idp3gcfegdlvrnp4cwq
    ONTO m1jm2qj3fnixrdn5qv7lcfgljb3taxbiy6o7uhf3xlykxbf7qve3ga
{
  ALTER SCALAR TYPE default::MessagePayload EXTENDING enum<Enrollment, Timer>;
};
