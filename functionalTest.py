import unittest
from picFromTaobao import *
from  FindItemUrl import *
import time
from Rules import *

class TestFindAllShopNewItemUrl(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		import shelve
		lookMoreUrlFile = shelve.open('lookMoreUrlFile')

		for i in list(lookMoreUrlFile.keys()):
			print(i)
		print(len(list(lookMoreUrlFile.keys())))

	def test_findAllShopNewItemUrl(self):
		findAllShopNewItemUrl()


class TestPostNewPicUrlFromItemUrl(unittest.TestCase):

	def setUp(self):
		import shelve
		self.ItemUrlFile = shelve.open('newItemUrl')

	def tearDown(self):
		self.pictureUrlFile = shelve.open('picturesUrlFile')
		print('new pictureUrl saved:')
		print(len(list(self.pictureUrlFile.keys())))

	def test_postNewPicUrlFromItemUrl(self):
		from multiprocessing import Pool
		pool = Pool(4)

		start = time.time()
		allNewItemUrlList = list(self.ItemUrlFile.keys())
		# allNewItemUrlList = []
		# for itemUrl in allItemUrlList:
		# 	if self.ItemUrlFile[itemUrl] == 'new':
		# 		allNewItemUrlList.append(itemUrl)

		print(len(allNewItemUrlList))
		print(allNewItemUrlList)
		pool.map(postNewPicUrlFromItemUrl, allNewItemUrlList)
		end = time.time()
		print('use: ' + str(end - start))
		self.assertEqual('foo'.upper(), 'FOO')

class TestFindItemsUrl(unittest.TestCase):

	def tearDown(self):
		self.itemUrlFile = shelve.open('newItemUrl')

		for i in list(self.itemUrlFile.keys()):
			print(i)
		print('new newItemUrl saved:')
		print(len(list(self.itemUrlFile.keys())))

	def test_findItemsUrl(self):
		lookMoreUrlFile = shelve.open('lookMoreUrlFile')
		pool = Pool(1)

		logging.basicConfig(filename='allShopNewItemUrl.log', filemode='w', level=logging.DEBUG)

		lookMoreUrlList = list(lookMoreUrlFile.keys())

		pool.map(findTodayNewItem, lookMoreUrlList)
		self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
	unittest.main()