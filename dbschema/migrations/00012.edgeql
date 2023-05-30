CREATE MIGRATION m1ynru4vda6bse2shqr7ydjig5jr25x5mklarhevxrb3ir5kvxwcha
    ONTO m1jhh4k36gyxjww66dn4czp5awrecbs2ics6p77avbm4cxafbbfcta
{
  ALTER SCALAR TYPE default::GameStatus EXTENDING enum<Enrollment, RoleAssignment, Night, Ended>;
};
