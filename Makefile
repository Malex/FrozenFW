DIR="${HOME}/maCMS/frozen/"

update:
	cat src/stdio.py | sed s/from\ __future__\ import\ print_function// > tmp.tmp
	cat tmp.tmp > src/stdio.py
	rm -f tmp.tmp

install:
	mkdir -p $(DIR)
	cp -R src/* $(DIR)
