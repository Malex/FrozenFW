import unittest

from frozen.File import File,FileError
from frozen.Sandbox import *

lol=1

class TestSand(unittest.TestCase):
	def setUp(self):
		File.set_limits("./*",["*miao.lol"],[r"frozen/File.py"])
		with open("tmp.txt",'w') as w:
			w.write("lol+=1")
		self.sandbox = Sandbox(["lol"],["./*",["*.txt"],["tmp.txt"]],)

	def test_limits(self):
		self.assertRaises(FileError,self.sandbox,"../.bashrc",glob=globals())
	def test_globals(self):
		self.sandbox("tmp.txt",glob=globals())
		self.assertEqual(lol,2)

if __name__=='__main__':
	unittest.main()
