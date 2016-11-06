import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.keys import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Rules import *

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

	for page in range(10):
		# scroll down to bottom
		for i in range(4):
			browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(3) # seconds
			print('scroll down to get more shop')
		# 点击下一页 
		browser.find_element_by_xpath("//a[@class='dpl-paginator-next J_NextPage J_HotPoint']").click()
		time.sleep(3)

		lookMoreClasses = browser.find_elements_by_link_text('查看更多')
		for lookMore in lookMoreClasses:
			allShopNewItemUrlList.append(lookMore.get_attribute('href'))
		
	return allShopNewItemUrlList


def saveAllShopNewItemUrl():
	pass


def findTodayNewItem(allShopNewItemUrlList, cookies):
	for lookMoreUrl in allShopNewItemUrlList:
		browser2 = webdriver.Firefox()
		browser2.get(lookMoreUrl)
		for cookie in cookies:
			browser2.add_cookie(cookie)
		browser2.get(lookMoreUrl)
		# 找到 上新 按钮
		shangXin = browser2.find_element_by_xpath("//ul[@class='gallery-album-menu-list clearfix']").find_element_by_tag_name('li').click()
		# browser2.quit()
		# 找到 上新日期 
		time.sleep(2)
		shangxinDate = browser2.find_element_by_xpath("//li[@class='gallery-album-title clearfix']")
	
		print(shangxinDate.text)
		browser2.quit()

# 保存item的URL 
def saveAllItemUrl(allShopNewItemUrlList):
	pass

	#店铺收藏
	# https://shoucang.taobao.com/shop_gallery_n.htm?spm=a1z0k.7385961.1997985009.1.cdcsr0&tab=4&cat=4&id=103845551&sellerId=1676877261&t=1478395652000
if __name__ == '__main__':
	allShopNewItemUrlList = findAllShopNewItemUrl()
	print(allShopNewItemUrlList)

	rules = Rules("allShopNewItemUrl")
	for itemUrl in allShopNewItemUrlList:
		rules.saveRule(itemUrl, "saved")