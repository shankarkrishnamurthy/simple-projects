query: query.l query.y
	flex query.l
	bison -d query.y
	gcc lex.yy.c query.tab.c -lfl -o query
clean:
	rm  -f lex.yy.c query.tab.* query a.out
