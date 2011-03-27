from setuptools import setup

setup(name="frozen",
		version="2.0-alpha",
		author="Malex",
		author_email="malexprojects@gmail.com",
		license="GNU/GPL3",
		description="A simple but cool framework for wsgi",
		packages=['frozen',"frozen.wsgi"],
		package_dir={"frozen":"frozen"},
		)
