all:
	gcc -fPIC -shared -o libmain.so main.c
	gcc -I /usr/include/python3.8/ c-2-py.c -lpython3.8 -o call
	gcc -I /usr/include/python3.8/ c-2-py-1.c  -lpython3.8 -o call-1
	python setup.py install --record files.txt # install 2 modules - record to remove
test:
	py-2-c.py # simple call from python to a C fn()
	@echo
	@echo "Calling pre existing py fn()"
	call-1
	@echo
	@echo "C -> python"
	PYTHONPATH=. call mult multiply 5 6
	@echo
	python -c "import emb; print(emb.numargs())"
	python -c "import hworld; print ( hworld.helloworld() )"
clean:
	rm -rf call* libmain.so build __*cache__ `cat files.txt` files.txt
