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
from db.itemUrlDb import itemUrlDb
from picFromTaobao import *

cookies = []


def getCookies():

	femalFavalUrl = 'https://shoucang.taobao.com/shop_collect_list_n.htm?spm=a1z0k.6846577.0.0.89UMIb&startRow=60&type=9&value=0%2C10000000000&tab=0&keyword=&t=1478331705580'
	browser = webdriver.PhantomJS()
	#browser = webdriver.Firefox()
	browser.get(femalFavalUrl)
	userName = 'tb6196862_2010'
	password = 'baobao&jinzi0913'
	try:
		browser.find_element_by_class_name('forget-pwdJ_Quick2Static').send_keys(Keys.ENTER)
	except NoSuchElementException as e:
		print('login error')

	browser.find_element_by_id('TPL_username_1').send_keys(userName)
	browser.find_element_by_id('TPL_password_1').send_keys(password)
	browser.find_element_by_id('J_SubmitStatic').send_keys(Keys.ENTER)
	print(browser.get_cookies())
	cookies = browser.get_cookies()
	return browser, cookies

def getShouChangCookies():

	femalFavalUrl = 'https://shoucang.taobao.com/shop_gallery_n.htm?id=36677438&cat=4&sellerId=72768346&tab=0'
	# browser = webdriver.PhantomJS()
	browser = webdriver.Firefox()
	browser.get(femalFavalUrl)
	userName = 'tb6196862_2010'
	password = 'baobao&jinzi0913'
	try:
		browser.find_element_by_class_name('forget-pwdJ_Quick2Static').send_keys(Keys.ENTER)
	except NoSuchElementException as e:
		print('login error')

	browser.find_element_by_id('TPL_username_1').send_keys(userName)
	browser.find_element_by_id('TPL_password_1').send_keys(password)
	browser.find_element_by_id('J_SubmitStatic').send_keys(Keys.ENTER)
	print(browser.get_cookies())
	cookies = browser.get_cookies()
	browser.quit()
	return cookies

def findAllShopNewItemUrl():
	global cookies
	import shelve
	lookMoreUrlFile = shelve.open('lookMoreUrlFile')
	allShopNewItemUrlList = []
	myDB = itemUrlDb('itemUrlDb')

	browser, cookies = getCookies()


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
				myDB.saveLookMoreUrl(lookMore.get_attribute('href'))
				# TODO: if url had been saved
				allShopNewItemUrlList.append(lookMore.get_attribute('href'))
			# 点击下一页
			browser.find_element_by_xpath("//a[@class='dpl-paginator-next J_NextPage J_HotPoint']").click()
			time.sleep(3)
		except NoSuchElementException as e:
			print('except:', e)
			logging.debug('get the last page %s, find %s shop item URL', page, len(allShopNewItemUrlList))
			break
	browser.quit()

	# for allShopNewItemUrl in allShopNewItemUrlList:
	# 	if not allShopNewItemUrl in lookMoreUrlFile.keys():
	# 		lookMoreUrlFile[allShopNewItemUrl] = 'saved'

def saveTodayNewItemUrl(lookMoreUrl, newItemUrlFile, cookies):
	myDB = itemUrlDb('itemUrlDb')
	print('lookMoreUrl:')
	print(lookMoreUrl)
	#browser = webdriver.PhantomJS()
	browser = webdriver.Firefox()
	# 先get，添加cookies后在get，否则报错
	browser.get(lookMoreUrl)
	for cookie in cookies:
		browser.add_cookie(cookie)
	browser.get(lookMoreUrl)
	try:
		# 找到 上新 按钮
		shangXin = browser.find_element_by_xpath(
			"//ul[@class='gallery-album-menu-list clearfix']").find_element_by_tag_name('li')
		shangXin.click()
	# browser2.quit()
	# 找到 上新日期
	except NoSuchElementException as e:
		print('shangXin url not matched')
		browser.quit()

	time.sleep(2)
	# shangxinDate = browser2.find_element_by_xpath("//li[@class='gallery-album-title clearfix']")
	try:
		shangxinDate = browser.find_element_by_xpath("//li[@class='gallery-album-title clearfix']")
		print(shangxinDate.text)

		#newItemUrlClassList = browser2.find_elements_by_xpath("//*[starts-with(name(), 'J_FavListItem g-gi-item fav-item fav-item-promotion')]")
		newItemUrlClassList = browser.find_elements_by_xpath("//div[@class='img-controller-img-box']")
		# save all the new item url,TODO: save new item by date
		if len(newItemUrlClassList) >= 1:
		#if len(newItemUrlClassList) >= 1 and shangxinDate.text.startswith('今天'):
			newItemCnt = int(shangXin.text.split()[-1], 10)
			print('begint to find new itemUrl')
			print(newItemCnt)
			for i in range(newItemCnt):
				print('find new itemUrl')
				newItemUrl = newItemUrlClassList[i].find_element_by_tag_name('a').get_attribute('href')
				print(newItemUrl)
				# TODO: save new item url
				# if not newItemUrl in newItemUrlFile:
				# 	newItemUrlFile[newItemUrl] = 'isToday'
				# 	print('save item url to local')
				# else:
				# 	print('had been saved.')
				if not myDB.queryIfItemUrlSaved(newItemUrl) == True:
					myDB.addItem(newItemUrl, 'saved')
					print('save item url')
				else:
					print('had been saved')


		else:
			print('Today no new item.')
	except NoSuchElementException as e:
		print('no shangxin')
		print('except:', e)
	except IndexError as e:
		print('except:', e)
	finally:
		print('finally quit browser.')
		browser.quit()

def findTodayNewItem(lookMoreUrl):

	import shelve
	newItemUrlFile = shelve.open('newItemUrl')
	with open('cookies.pickle', 'rb') as f:
		cookies = pickle.load(f)

	saveTodayNewItemUrl(lookMoreUrl, newItemUrlFile, cookies)

if __name__ == '__main__':

	cookies = getShouChangCookies()
	print(cookies)

	import pickle
	with open('cookies.pickle', 'wb') as f:
		pickle.dump(cookies, f)

	with open('cookies.pickle', 'rb') as f:
		data = pickle.load(f)
		print(data)


