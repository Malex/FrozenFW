DIR="${HOME}/prova/miao/"

update:
	cat src/conf.py | sed s/anydbm/dbm/ >> src/conf.py

install:
	mkdir -p $(DIR)
	cp -R src/* $(DIR)
