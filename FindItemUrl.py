import pickle
import time
import logging
from builtins import print
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Rules import *
from picFromTaobao import *

def findAllShopNewItemUrl():
	allShopNewItemUrlList = []

	femalFavalUrl = 'https://shoucang.taobao.com/shop_collect_list_n.htm?spm=a1z0k.6846577.0.0.89UMIb&startRow=60&type=9&value=0%2C10000000000&tab=0&keyword=&t=1478331705580'
	lookMoreClassName = 'item-list-more-btn J_PopRecTrigLink J_NewPoint'
	browser = webdriver.Firefox()
	browser.get(femalFavalUrl)

	userName = 'tb6196862_2010'
	password = 'baobao&jinzi0913'
	browser.find_element_by_id('TPL_username_1').send_keys(userName)
	browser.find_element_by_id('TPL_password_1').send_keys(password)
	browser.find_element_by_id('J_SubmitStatic').send_keys(Keys.ENTER)
	print(browser.get_cookies())
	cookies = browser.get_cookies()

	for page in range(100):
		# scroll down to bottom
		for i in range(3):
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(3) # seconds
			print('scroll down to get more shop')
		try:
			lookMoreClasses = browser.find_elements_by_link_text('查看更多')
			logging.debug('found %s lookMoreUrl in page %', len(lookMoreClasses), page)
			print('found ' + str(len(lookMoreClasses)) + ' lookMoreUrl in page ' + str(page))
			for lookMore in lookMoreClasses:
				allShopNewItemUrlList.append(lookMore.get_attribute('href'))
			# 点击下一页
			browser.find_element_by_xpath("//a[@class='dpl-paginator-next J_NextPage J_HotPoint']").click()
			time.sleep(3)
		except NoSuchElementException as e:
			print('except:', e)
			logging.debug('get the last page %s, find %s shop item URL', page, len(allShopNewItemUrlList))
			break

	return allShopNewItemUrlList, cookies


def saveAllShopNewItemUrl():
	pass


def findTodayNewItem(allShopNewItemUrlList):
	newItemUrlList = []

	femalFavalUrl = 'https://shoucang.taobao.com/shop_collect_list_n.htm?spm=a1z0k.6846577.0.0.89UMIb&startRow=60&type=9&value=0%2C10000000000&tab=0&keyword=&t=1478331705580'
	lookMoreClassName = 'item-list-more-btn J_PopRecTrigLink J_NewPoint'
	browser = webdriver.Firefox()
	browser.get(femalFavalUrl)

	userName = 'tb6196862_2010'
	password = 'baobao&jinzi0913'
	browser.find_element_by_id('TPL_username_1').send_keys(userName)
	browser.find_element_by_id('TPL_password_1').send_keys(password)
	browser.find_element_by_id('J_SubmitStatic').send_keys(Keys.ENTER)
	print(browser.get_cookies())
	cookies = browser.get_cookies()

	for lookMoreUrl in allShopNewItemUrlList:
		print('lookMoreUrl:')
		print(lookMoreUrl)
		browser2 = webdriver.Firefox()
		browser2.get(lookMoreUrl)
		for cookie in cookies:
			browser2.add_cookie(cookie)
		browser2.get(lookMoreUrl)
		try:
			# 找到 上新 按钮
			shangXin = browser2.find_element_by_xpath("//ul[@class='gallery-album-menu-list clearfix']").find_element_by_tag_name('li')
			shangXin.click()
			# browser2.quit()
			# 找到 上新日期
		except NoSuchElementException as e:
			print('shangXin url not matched')
			browser2.quit()
			break
		time.sleep(2)
		#shangxinDate = browser2.find_element_by_xpath("//li[@class='gallery-album-title clearfix']")
		try:
			shangxinDate = browser2.find_element_by_xpath("//li[@class='gallery-album-title clearfix']")
			print(shangxinDate.text)

			#newItemUrlClassList = browser2.find_elements_by_xpath("//*[starts-with(name(), 'J_FavListItem g-gi-item fav-item fav-item-promotion')]")
			newItemUrlClassList = browser2.find_elements_by_xpath("//div[@class='img-controller-img-box']")
			# save all the new item url,TODO: save new item by date
			if len(newItemUrlClassList) >= 1 and shangxinDate.text.startswith('今天'):
				newItemCnt = int(shangXin.text.split()[-1], 10)
				print('begint to find new itemUrl')
				for i in range(newItemCnt):
					print('find new itemUrl')
					newItemUrl = newItemUrlClassList[i].find_element_by_tag_name('a').get_attribute('href')
					print(newItemUrl)
					newItemUrlList.append(newItemUrl)
			browser2.quit()

		except NoSuchElementException as e:
			print('no shangxin')
			print('except:', e)
			browser2.quit()
		except IndexError as e:
			print('except:', e)
			browser2.quit()
		#//*[starts-with(name(),'B')]
		#//*[contains(name(),'B')]
	print(newItemUrlList)
	return newItemUrlList


# 保存item的URL 
def saveAllNewItemUrl(allShopNewItemUrlList):
	pass

def saveAllShopCollectUrl(allShopNewItemUrlList):
	pass

	#店铺收藏
	# https://shoucang.taobao.com/shop_gallery_n.htm?spm=a1z0k.7385961.1997985009.1.cdcsr0&tab=4&cat=4&id=103845551&sellerId=1676877261&t=1478395652000
if __name__ == '__main__':

	allShopNewItemUrlList = []
	allNewItemUrlList = []
	shopCollectUrlFile = Rules('ShopCollectUrl')

	import shelve
	newItemUrlFile = shelve.open('newItemUrl')

	logging.basicConfig(filename='allShopNewItemUrl.log', filemode='w', level=logging.DEBUG)

	print(shopCollectUrlFile.loadValue('https://item.taobao.com/item.htm?id=539898810329&_u='))

	# allShopNewItemUrlList, cookies = findAllShopNewItemUrl()
	# print(allShopNewItemUrlList)
	# for itemUrl in allShopNewItemUrlList:
	# 	shopCollectUrlFile.saveRule(itemUrl, "saved")
	#
	# print(len(shopCollectUrlFile.getAllKeysList()))
	#
	#
	# allShopNewItemUrlList = shopCollectUrlFile.getAllKeysList()
	# allNewItemUrlList = findTodayNewItem(allShopNewItemUrlList)
	#
	# for newItemUrl in allNewItemUrlList:
	# 	print(newItemUrl)
	# 	newItemUrlFile[newItemUrl] = "saved"

	allNewItemUrlList = list(newItemUrlFile.keys())
	print(len(allNewItemUrlList))
	getPicUrlFromItemUrl(allNewItemUrlList)


