DIR="${HOME}/maCMS/frozen/"

update:
	cat src/std.py | sed s/from\ __future__\ import\ print_function// > tmp.tmp
	cat tmp.tmp > src/std.py
	rm -f tmp.tmp

install:
	mkdir -p $(DIR)
	cp -R src/* $(DIR)
