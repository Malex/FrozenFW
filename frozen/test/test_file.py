import unittest

from frozen.File import *


class FileTest(unittest.TestCase):

	def setUp(self):
		File.set_limits(r"\./.*",[r".*miao\.lol"],[r"frozen/File.py"])

	def test_limit(self):
		self.assertRaises(FileError,open,"../hahahaha")
		self.assertEqual(open("frozen/File.py").read(),__builtins__.open("frozen/File.py").read())

	def test_blacklist(self):
		self.assertRaises(FileError,open,"./miao.lol")
	def test_getContents(self):
		self.assertEqual(File.get_contents("frozen/File.py"),open("frozen/File.py").read())

if __name__=='__main__':
	unittest.main()

