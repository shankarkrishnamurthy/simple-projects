/*
    Description: Simple skeleton grammer for a query (similar to JIRA Query)
    Without any comparison to key-value pairs.
    Author: Shankar, K
    Date: Jun 2020
    Example:
        # cat /tmp/test 
        (a=b && (c>3 | d!=10))
        # query /tmp/test
        ...

*/

%{
#include<stdio.h>
#include<stdlib.h>
extern FILE *yyin;
int yyerror (char *s);
int yylex();
int scmp(char*a,char*b,char*c);
int ncmp(char*a,char*b,char*c);
int lcmp(int a,char*b,int c);
%}

%left "(" ")"
%token <s>LOP <s>CMP <s>NUM <s>STR <s>HEX <s>ERR <s>OPP <s>CLP ENDF
%union
{
    int n;
    char *s;
}
%type <n> query
%type <n> done
%type <n> expr
%%

done: 
    query '\n'          {printf("Result %d\n", $1); return 0;} 
    | query ENDF        {printf("EOF\n"); exit(0);}
query:
    %empty              {$$=1;}      
    | query LOP expr    {$$=lcmp($1, $2, $3);printf("Q-%d\n",$$);}
    | expr              {$$=$1;} /*redundant*/
    ;

expr:   
    STR CMP STR         {$$=scmp($1,$2,$3);printf("ES-%d\n",$$);}
    | STR CMP NUM       {$$=ncmp($1,$2,$3);printf("EN-%d\n",$$);}
    | OPP query CLP     { $$=$2; }
    ;
%%

int scmp(char*a,char*b,char*c) { printf("%s %s %s\n", a,b,c);return 0;}
int ncmp(char*a,char*b,char*c) { printf("%s %s %s\n", a,b,c);return 0;}
int lcmp(int a,char*b,int c) {printf("%d %s %d\n", a,b,c);return 0; }

int main(int argc, char **argv)
{
    if (argc > 1) yyin = fopen(argv[1], "r");
    while (0 == yyparse()); /* returns when token 0 is seen from flex/scanner */
    if (argc > 1) fclose(yyin);

    return 0;
}


