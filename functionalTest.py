import unittest
from db.itemUrlDb import itemUrlDb
from picFromTaobao import *
from  FindItemUrl import *
import time
from Rules import *
from multiprocessing import Pool

class TestFindAllShopNewItemUrl(unittest.TestCase):

	def setUp(self):
		self.myDB = itemUrlDb('itemUrl.db')

	def tearDown(self):
		urlList = self.myDB.queryAllLookMoreUrl()
		print(len(urlList))
		for i in urlList:
			print(i)

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
		pool = Pool(2)

		start = time.time()
		allNewItemUrlList = list(self.ItemUrlFile.keys())
		# allNewItemUrlList = []
		# for itemUrl in allItemUrlList:
		# 	if self.ItemUrlFile[itemUrl] == 'new':
		# 		allNewItemUrlList.append(itemUrl)

		print(len(allNewItemUrlList))
		print(allNewItemUrlList)
		pool.map(postNewPicUrlFromItemUrl, allNewItemUrlList[:20])
		end = time.time()
		#print('use: ' + str(end - start))
		self.assertEqual('foo'.upper(), 'FOO')

class TestFindItemsUrl(unittest.TestCase):

	def setUp(self):
		# cookies = getShouChangCookies()
		# print('cookies: ')
		# print(cookies)
		# import pickle
		# with open('cookies.pickle', 'wb') as f:
		# 	pickle.dump(cookies, f)
		# with open('cookies.pickle', 'rb') as f:
		# 	self.assertEqual(pickle.load(f), cookies)
		#
		self.myDB = itemUrlDb('itemUrl.db')
		self.lookMoreUrlList = self.myDB.queryAllLookMoreUrl()
		for i in self.lookMoreUrlList:
			print(i)

	def tearDown(self):
		# self.itemUrlFile = shelve.open('newItemUrl')
		#
		# for i in list(self.itemUrlFile.keys()):
		# 	print(i)
		# print('new newItemUrl saved:')
		# print(len(list(self.itemUrlFile.keys())))

		itemList = self.myDB.queryAllItems()
		print(len(itemList))
		for i in itemList:
			print(i)

	def test_findItemsUrl(self):

		pool = Pool(2)

		logging.basicConfig(filename='allShopNewItemUrl.log', filemode='w', level=logging.DEBUG)

		pool.map(findTodayNewItem, self.lookMoreUrlList[:10])
		self.assertEqual('foo'.upper(), 'FOO')

class TestItemUrlDb(unittest.TestCase):

	def setUp(self):
		self.picUrl = 'https://gd1.alicdn.com/imgextra/i3/0/TB10lxmNVXXXXbiXFXXXXXXXXXX_!!0-item_pic.jpg_400x400.jpg'
		self.myDB = itemUrlDb('itemUrlDb')

	def tearDown(self):
		self.myDB.deleteItem(self.picUrl)
		self.myDB.c.execute("DELETE FROM lookMoreUrlTable WHERE lookMoreUrl = '%s'" % self.picUrl)

	def test_itemUrlDb(self):

		self.myDB.addItem(self.picUrl, 'saved')
		isNew = self.myDB.queryIfItemUrlSaved(self.picUrl)
		self.assertEqual(isNew, True)

		itemList = self.myDB.queryAllItems()
		self.assertEqual(itemList, [(self.picUrl,)])

	def test_lookMoreUrl(self):
		self.myDB.saveLookMoreUrl(self.picUrl)
		urlList = self.myDB.queryAllLookMoreUrl()
		self.assertEqual(len(urlList), 1)

if __name__ == '__main__':
	unittest.main()