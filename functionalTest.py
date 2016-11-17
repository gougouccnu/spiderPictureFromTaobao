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
		self.myDB = itemUrlDb('itemUrlDb')

	def tearDown(self):
		for url in self.myDB.queryAllPictureUrl():
			print(url)
		self.myDB.close()

	def test_postNewPicUrlFromItemUrl(self):
		pool = Pool(4)

		allNewItemUrlList = self.myDB.queryAllTodayItem()

		print(len(allNewItemUrlList))
		print(allNewItemUrlList)
		pool.map(postNewPicUrlFromItemUrl, allNewItemUrlList[:100])
		self.assertEqual('foo'.upper(), 'FOO')

class TestFindItemsUrl(unittest.TestCase):

	def setUp(self):
		cookies = getShouChangCookies()
		print('cookies: ')
		print(cookies)
		import pickle
		with open('cookies.pickle', 'wb') as f:
			pickle.dump(cookies, f)
		with open('cookies.pickle', 'rb') as f:
			self.assertEqual(pickle.load(f), cookies)

		self.myDB = itemUrlDb('itemUrlDb')
		self.lookMoreUrlList = []
		for i in self.myDB.queryAllLookMoreUrl():
			self.lookMoreUrlList.append(i[0])


	def tearDown(self):
		#clear data
		itemList = self.myDB.queryAllItems()
		for i in itemList:
			print(i)
			self.myDB.deleteItem(i)

		itemPicUrlList = self.myDB.queryAllPictureUrl()
		for i in itemPicUrlList:
			print(i)
			self.myDB.deletePictureUrl(i)
		print(len(itemList))
		print(len(itemPicUrlList))

		self.myDB.close()

	def test_findItemsUrl(self):

		pool = Pool(1)

		logging.basicConfig(filename='allShopNewItemUrl.log', filemode='w', level=logging.DEBUG)

		pool.map(findTodayNewItem, self.lookMoreUrlList[:4])
		self.assertEqual('foo'.upper(), 'FOO')

class TestItemUrlDb(unittest.TestCase):

	def setUp(self):
		self.picUrl = 'https://gd1.alicdn.com/imgextra/i3/0/TB10lxmNVXXXXbiXFXXXXXXXXXX_!!0-item_pic.jpg_400x400.jpg'
		self.myDB = itemUrlDb('itemUrlDb')

	def tearDown(self):
		self.myDB.deleteItem(self.picUrl)

	def test_itemUrlDb(self):

		self.myDB.addItem(self.picUrl, 'saved')
		isNew = self.myDB.queryIfItemUrlSaved(self.picUrl)
		self.assertEqual(isNew, True)

		itemList = self.myDB.queryAllItems()
		self.assertIn(self.picUrl, itemList)

		self.myDB.addItem(self.picUrl, 'today')
		self.assertIn(self.picUrl, self.myDB.queryAllTodayItem())


	def test_lookMoreUrl(self):
		self.myDB.saveLookMoreUrl(self.picUrl)
		urlList = self.myDB.queryAllLookMoreUrl()
		self.assertEqual(len(urlList), 1)

	def test_pictureUrlDb(self):
		self.myDB.addPictureUrl(self.picUrl)
		self.assertIn(self.picUrl, self.myDB.queryAllPictureUrl())
		self.assertEqual(self.myDB.queryIfPicUrlUpload(self.picUrl), True)

if __name__ == '__main__':
	unittest.main()