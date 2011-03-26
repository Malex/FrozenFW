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
		self.conf = Conf("conf.test.txt")

	def tearDown(self):
		os.unlink("conf.test.txt")

	def test_var(self):
		self.assertEqual(conf.query("allow_miao","lol"))
	def test_if(self):
		self.assertTrue(conf.query("works"))
	def test_chain(self):
		self.assertTrue(conf.query("test"))


if __name__=='__main__':
	unittest.main()
