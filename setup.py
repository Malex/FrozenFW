from setuptools import setup

setup(name = "frozen",
		version = "2.0-alpha",
		author = "Malex",
		author_email = "malexprojects@gmail.com",
		maintainer = "Malex",
		maintainer_email = "malexprojects@gmail.com",
		license = "GNU/GPL3",
		description = "A simple but cool framework for wsgi",
		long_description = "It provides lots of classes and functions for web developing, using wsgi interface and a cool plugin system",
		url = "http://malexprojects.ath.cx/?p=frozen",
		download_url = "http://malexprojects.ath.cx/?d=frozen",
		platforms = "any",
		packages = ['frozen',"frozen.wsgi","frozen.test",],
		package_dir = { "frozen" : "frozen",},
		classifiers = ["Development Status :: 2 - Pre-Alpha", "Enviroment :: Other Enviroment", "Intended Audience :: Developers",
						"License :: OSI Approved :: GNU General Public License (GPL)", "Natural Language :: English",
						"Operating System :: OS Indipendent", "Programming Language :: Python :: 3.1",
						"Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",],
		keywords = [ "web", "framework", "template", "wsgi", ],
		)
