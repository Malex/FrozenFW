import unittest,os
from ..Conf import *

class TestConf(unittest.TestCase):

	t = """
allow_miao = "lol"
if not __name__=="__main__":
	works = True
conf_chain = "./lol.txt"
"""
	lol = """
test=True
"""

	def setUp(self):
		with open("conf.test.txt",'w') as w:
			w.write(self.t)
		with open("./lol.txt",'w') as w:
			w.write(self.lol)
		self.conf = Conf("conf.test.txt")

	def tearDown(self):
		os.system("rm conf.test.txt")
		os.system("rm ./lol.txt")

	def test_var(self):
		self.assertEqual(self.conf.query("allow_miao"),"lol")
	def test_if(self):
		self.assertTrue(self.conf.query("works"))
	def test_chain(self):
		self.assertTrue(self.conf.query("test"))


if __name__=='__main__':
	unittest.main()
