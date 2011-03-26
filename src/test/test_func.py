import unittest

from frozen.functions import *

class KindTest(unittest.TestCase):
	def test_nl2br(self):
		self.assertEqual(nl2br("lol\ngay"),"lol<br />gay")
	def test_html(self):
		self.assertEqual(htmlspecialchars("\"<>'&"),"&quot;&lt;&gt;&#039;&amp;")
		## htmlentities

if __name__=='__main__':
	unittest.main()
