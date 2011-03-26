import unittest

from frozen.File import *


class FileTest(unittest.TestCase):

	def setUp(self):
		File.set_limits(r"\./.*",[r".*miao\.lol"],[r"src/File.py"])

	def test_limit(self):
		self.assertRaises(FileError,open,"../hahahaha")
		self.assertEqual(open("src/File.py").read(),__builtins__.open("src/File.py").read())

	def test_blacklist(self):
		self.assertRaises(FileError,open,"./miao.lol")
	def test_getContents(self):
		self.assertEqual(File.get_contents("src/File.py"),open("src/File.py").read())

if __name__=='__main__':
	unittest.main()

