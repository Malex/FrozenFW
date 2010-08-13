DIR="/usr/lib/python3.1/site-packages/frozen"


install:
	mkdir -p /tmp/frozen/
	cp -R * /tmp/frozen/
	cd /tmp/frozen/src; patch < __init__.py.patch
	mkdir -p $(DIR)
	cp -R /tmp/frozen/src/* $(DIR)
