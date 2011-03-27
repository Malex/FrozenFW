import unittest

from frozen.Logger import *

class LoggerTest(unittest.TestCase):
	def setUp(self):
		self.log = Logger("tmp.txt",NOTICE)
	def test_error(self):
		try:
			raise ValueError("prova")
		except BaseException as e:
			self.log.write(e)
		finally:
			with open("tmp.txt") as f:
				self.assertRegexpMatches(f.read(),".+File\s\w+\.py\sLine\s\w+\s=>\s.+?:\s.+\s")
	def test_notice(self):
		self.log.notice("It's a joke")
		with open("tmp.txt") as f:
			self.assertRegexpMatches(f.readlines()[-1],r".+It's a joke")

if __name__=='__main__':
	unittest.main()
