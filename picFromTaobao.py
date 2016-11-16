# -*- coding: utf8 -*-
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import *
import csv
import time
import urllib.request
import os.path
import os

import argparse
import re
from multiprocessing import Pool
import io
from Rules import *
from accessBmobPy3 import *
from Rules import *
from db.itemUrlDb import itemUrlDb


def getItemsUrl(driver):
	itemUrlList = []
	div = driver.find_element_by_xpath("//div[@class='shop-hesper-bd grid']")
	items = div.find_elements_by_class_name('item3line1')
	for item in items:
		for dl in item.find_elements_by_tag_name('dl'):
			try:
				itemUrl = dl.find_element_by_class_name('detail').find_element_by_tag_name('a').get_attribute('href')
				print(itemUrl)
				itemUrlList.append(itemUrl)
			except NoSuchElementException as e:
				print('except:', e)
	return itemUrlList

def getImgBigSrc(imgSrc):
	return imgSrc.replace('50x50', '400x400')

def saveImg(path, url, name):
	print('save img: ' + path + '/' + name)
	conn = urllib.request.urlopen(url)
	try:
		f = open(path + '/' + name, 'wb')
		f.write(conn.read())
		f.close()
	except e:
		print(e)

def saveImgUrlToCsv(FILE_NAME, itemUrl, imgBigSrc):
	with open(FILE_NAME, 'a') as csvfile:
		fieldnames = ['itemUrl', 'imgBigUrl']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writerow({'itemUrl': itemUrl, 'imgBigUrl': imgBigSrc})
				
def saveImgToBmob(USER_ID, imgBigUrl, itemUrl):
	url = 'api.bmob.cn'
	table = 'picInf'
	
	totalData = json.dumps({
		"picUrl":imgBigUrl, 
		"itemUrl":itemUrl, 
		"user":{"__type":"Pointer","className":"_User","objectId":USER_ID},
		"starter":{"__type":"Pointer","className":"_User","objectId":"none"}
		})
	postToBmob(url, table, totalData)

def getPicturesUrl(driver, itemUrl):
	picturesUrlList = []

	logging.debug('try to get pictures from URL: %s ', itemUrl)
	try:
		ul = driver.find_element_by_xpath("//ul[@class='tb-thumb tb-clearfix']")
	except NoSuchElementException as e:
		print('not match pic url')
		return
	for li in ul.find_elements_by_tag_name('li'):
		try:
			imgSrc = li.find_element_by_tag_name('img').get_attribute('src')
			print(imgSrc)
			imgBigSrc = getImgBigSrc(imgSrc)
			print('After convert:\n')
			print(imgBigSrc)
			picturesUrlList.append(imgBigSrc)
		except NoSuchElementException as e:
			print('except:', e)
			logging.debug('NoSuchElementException occur: %s ', e.msg)

	return picturesUrlList

def PostNewPicturesUrl(driver, itemUrl):

	myDB = itemUrlDb('itemUrlDb')
	USER_ID = 'JLkR444G'
	logging.debug('try to get pictures from URL: %s ', itemUrl)

	picturesUrlList = getPicturesUrl(driver, itemUrl)
	print(picturesUrlList)
	if picturesUrlList == None:
		return
	for picturesUrl in picturesUrlList:

		if myDB.queryIfPicUrlUpload(picturesUrl):

		# if picturesUrl in picturesUrlFile.keys():
		# 	if picturesUrlFile[picturesUrl] == 'uploaded':
			logging.debug('had been post to bmob')
			print('had been post to bmob')
			return
		#saveImgToBmob(USER_ID, picturesUrl, itemUrl)
		# 保存到数据库
		print('faked post to bmob')
		#picturesUrlFile[picturesUrl] = 'uploaded'
		myDB.addPictureUrl(picturesUrl)

	myDB.addItem(itemUrl, 'saved')

def postNewPicUrlFromItemUrl(itemUrl):
	print('item url:')
	print(itemUrl)
	#if itemUrlFile[itemUrl] == 'isToday':
	#if myDB.queryIfItemUrlSavedToday(itemUrl):
	#browser = webdriver.PhantomJS()
	browser = webdriver.Firefox()
	browser.get(itemUrl)
	PostNewPicturesUrl(browser, itemUrl)
	browser.quit()

def getPicFromShop(shopUrl):
	browser = webdriver.PhantomJS()
	browser.get(shopUrl)

	shopName = browser.find_element_by_xpath("//span[@class='shop-name']").find_element_by_tag_name('a').text
	itemUrlList = getItemsUrl(browser)
	postNewPicUrlFromItemUrl(itemUrlList, shopName)

	browser.quit()