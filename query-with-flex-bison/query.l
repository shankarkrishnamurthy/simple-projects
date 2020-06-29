%{
#include<stdio.h>
#include "query.tab.h"

%}
%option noyywrap yylineno nodefault

%%

"||"|"|"|"&&"|"&"                       {return LOP;}
">="|">"|"<"|"<="|"="|"!="|"=="         {return CMP;}
[0-9]+                                  {return NUM;}
[a-zA-z]+                               {return STR;}
0x[0-9a-fA-F]                           {return HEX;}
"("                                     {printf("OPP\n");return OPP;}
")"                                     {return CLP;}
[ \t]                                   {}
[\n.]                                   {return yytext[0];}

%%

#if 0
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


int yyerror(char *s)
{
    fprintf(stderr, "error %d: %s at %s\n", yylineno, s, yytext);
    return 0;
}

