PYTHON="python3.1"
DIR="/home/malex/pymod/frozen"

install:
	cp -R src/* $(DIR)

cgi:
	mkdir -p /tmp/frozen/
	cp -R * /tmp/frozen/
	cd /tmp/frozen/src; patch < __init__.py.patch
	mkdir -p $(DIR)
	cp -R /tmp/frozen/src/* $(DIR)
