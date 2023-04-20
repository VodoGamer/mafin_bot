CREATE MIGRATION m1q6octrftdfl3z3cjiwit2wlimvjoo777xnjllbl3nd57chq54bbq
    ONTO m1lnviymkresjhf2xv7tggfai4b743uqdp3ppwbv57nnzqadopnnuq
{
  ALTER TYPE default::Game {
      ALTER PROPERTY start_date {
          RENAME TO start_date;
      };
  };
  ALTER TYPE default::Game {
      ALTER PROPERTY  {
          RENAME TO status;
      };
  };
};
