CREATE MIGRATION m1jhh4k36gyxjww66dn4czp5awrecbs2ics6p77avbm4cxafbbfcta
    ONTO m13hxh4bxazl4rfogadwevswrbeep7iu527wm535slmselk6g2ed6a
{
  ALTER SCALAR TYPE default::GameStatus EXTENDING enum<Enrollment, RoleAssignment, Ended>;
};
