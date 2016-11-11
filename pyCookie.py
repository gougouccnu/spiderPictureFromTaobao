import pickle
import time
from selenium import webdriver
from selenium.webdriver.common.keys import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def findAllShopNewItemUrl():
	femalFavalUrl = 'https://shoucang.taobao.com/shop_collect_list_n.htm?spm=a1z0k.6846577.0.0.89UMIb&startRow=60&type=9&value=0%2C10000000000&tab=0&keyword=&t=1478331705580'
	lookMoreClassName = 'item-list-more-btn J_PopRecTrigLink J_NewPoint'
	browser = webdriver.PhantomJS()
	browser.get(femalFavalUrl)

	userName = 'tb6196862_2010'
	password = 'baobao&jinzi0913'
	browser.find_element_by_id('TPL_username_1').send_keys(userName)
	browser.find_element_by_id('TPL_password_1').send_keys(password)
	browser.find_element_by_id('J_SubmitStatic').send_keys(Keys.ENTER)
	print(browser.get_cookies())
	cookies = browser.get_cookies()
	# scroll down to bottom
	for i in range(2):
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(3) # seconds
		print('&'*10)
	lookMoreClasses = browser.find_elements_by_link_text('查看更多')

def saveAllShopNewItemUrl():
	pass


def findTodayNewItem(lookMoreClasses):
	for lookMore in lookMoreClasses:
		lookMoreUrl = lookMore.get_attribute('href')
		print(lookMoreUrl)
		print('*'*9)
		browser2 = webdriver.PhantomJS()
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
def saveAllItemUrl():
	pass

	#店铺收藏
	# https://shoucang.taobao.com/shop_gallery_n.htm?spm=a1z0k.7385961.1997985009.1.cdcsr0&tab=4&cat=4&id=103845551&sellerId=1676877261&t=1478395652000
