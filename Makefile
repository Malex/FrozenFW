DIR="${HOME}/maCMS/"

update:
	cat src/conf.py | sed s/anydbm/dbm/ > tmp.tmp
	cat tmp.tmp > src/conf.py
	rm tmp.tmp

install:
	mkdir -p $(DIR)
	cp -R src/* $(DIR)
