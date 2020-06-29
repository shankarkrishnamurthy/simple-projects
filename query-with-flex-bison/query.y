%{
#include<stdio.h>
#include<stdlib.h>
extern FILE *yyin;
int yyerror (char *s);
int yylex();
%}

%token LOP CMP NUM STR HEX ERR OPP CLP

%%

done: query '\n'        {printf("Result %d\n", $1); exit(0);}
query:
    | query LOP expr    {printf("RED1\n");}
    | expr              {printf("RED2\n");}
    ;

expr:   
    | STR CMP STR       {printf("STR CMP STR\n");}
    | STR CMP NUM       {printf("STR CMP NUM\n");}
    | OPP query CLP     {printf("( TERM )\n"); } // not working
    ;
%%

int main(int argc, char **argv)
{
    if (argc > 1) yyin = fopen(argv[1], "r");
    yyparse(); /* returns when token 0 is seen from flex/scanner */
    if (argc > 1) fclose(yyin);

    return 0;
}


