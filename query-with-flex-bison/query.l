/*
    Description: Simple lexical anaylyzer for a query (similar to JIRA Query)
    Author: Shankar, K
    Date: Jun 2020
*/
%{
#include<stdio.h>
#include<string.h>
#include "query.tab.h" // Redefinition/Independent definition leads to weird problems
%}
%option noyywrap yylineno nodefault

%%

<<EOF>>                                 {return ENDF; /* ^D for stdin (or) EOF for file */}
"||"|"|"|"&&"|"&"                       {yylval.s = strdup(yytext);return LOP;}
">="|">"|"<"|"<="|"="|"!="|"=="         {yylval.s = strdup(yytext);return CMP;}
[0-9]+                                  {yylval.s = strdup(yytext);return NUM;}
[a-zA-z]+                               {yylval.s = strdup(yytext);return STR;}
0x[0-9a-fA-F]                           {yylval.s = strdup(yytext);return HEX;}
"("                                     {yylval.s = strdup(yytext);return OPP;}
")"                                     {yylval.s = strdup(yytext);return CLP;}
[ \t]                                   {}
.|\n                                    {yylval.s = strdup(yytext);return yytext[0];}
%%

int yyerror(char *s)
{
    fprintf(stderr, "error %d: %s at %s\n", yylineno, s, yytext);
    return 0;
}

#if STAND_ALONE_LEX
static int process()
{
    int rc;
	while((rc=yylex()) != 0) {
           printf("%d %s\n", rc, yytext);
    }
}

int main(int argc, char **argv) 
{
    if (argc == 1) {
        process();
        goto end;
    }

	FILE *fptr = fopen(argv[1], "r");
    if (!fptr) { printf("Invalid File %s\n", argv[1]); goto end; }
	yyrestart(fptr);
    process();
	fclose(fptr);
end:
	return 0;
}
#endif


