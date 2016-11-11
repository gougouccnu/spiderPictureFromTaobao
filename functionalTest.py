import unittest
from picFromTaobao import *
from  FindItemUrl import *
import time

class TestStringMethods(unittest.TestCase):

	def test_upper(self):
		self.assertEqual('foo'.upper(), 'FOO')

	def test_isupper(self):
		self.assertTrue('FOO'.isupper())
		self.assertFalse('Foo'.isupper())

	def test_split(self):
		s = 'hello world'
		self.assertEqual(s.split(), ['hello', 'world'])
		# check that s.split fails when the separator is not a string
		with self.assertRaises(TypeError):
			s.split(2)

class TestFindItemUrl(unittest.TestCase):

	def setUp(self):
		import shelve
		self.newItemUrlFile = shelve.open('newItemUrl')

	def test_findItemUrl(self):
		from multiprocessing import Pool
		pool = Pool(4)

		start = time.time()
		allNewItemUrlList = list(self.newItemUrlFile.keys())
		print(len(allNewItemUrlList))
		print(allNewItemUrlList)
		pool.map(getPicUrlFromItemUrl, allNewItemUrlList)
		end = time.time()
		print('use: ' + str(end - start))
		self.assertEqual('foo'.upper(), 'FOO')

class TestFindNewItemUrl(unittest.TestCase):

	def test_findNewItemUrl(self):
		shopCollectUrlFile = Rules('ShopCollectUrl')
		pool = Pool(4)

		logging.basicConfig(filename='allShopNewItemUrl.log', filemode='w', level=logging.DEBUG)

		allShopNewItemUrlList = shopCollectUrlFile.getAllKeysList()
		for allShopNewItemUrl in allShopNewItemUrlList:
			print(allShopNewItemUrl)
		pool.map(findTodayNewItem, allShopNewItemUrlList)
		self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
	unittest.main()