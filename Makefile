DIR="/usr/lib/python3.1/site-package/"


install:
	patch < src/__init__.py.patch
	mkdir -p $(DIR)
	cp -R src/* $(DIR)
