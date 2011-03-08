from ..Cookie import *
import random
from string import ascii_letters,digits

avaiable_chars = ascii_letters+digits

class Session(Cookie):
	__id = ""

	def __init__(self, expires :int =60 ):
		i = (random.randint(a,65) for a in xrange(0,65))
		for j in i:
			self.__id += str(avaiable_chars[j])
		super().__init__("pysessid",self.__id,expires,httpOnly=True)

	@property
	def id(self):
		return self.__id
