import unittest

from frozen.File import *


class FileTest(unittest.TestCase):

	def setUp(self):
		File.base_dir = "./"
		File.set_limits("./*",["*.py"],["frozen/File.py"])

	def test_limit(self):
		self.assertRaises(FileError,File.open,"../.bashrc")
		self.assertEqual(open("frozen/File.py").read(),__builtins__.open("frozen/File.py").read())

	def test_blacklist(self):
		self.assertRaises(FileError,open,"./frozen/Conf.py")
	def test_getContents(self):
		self.assertEqual(File.get_contents("frozen/File.py"),open("frozen/File.py").read())

if __name__=='__main__':
	unittest.main()

