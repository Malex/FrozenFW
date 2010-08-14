PYTHON="python3.1"
DIR="/usr/lib/$(PYTHON)/site-packages/frozen"

cgi:
	cp -R src/* $(DIR)

install:
	mkdir -p /tmp/frozen/
	cp -R * /tmp/frozen/
	cd /tmp/frozen/src; patch < __init__.py.patch
	mkdir -p $(DIR)
	cp -R /tmp/frozen/src/* $(DIR)
