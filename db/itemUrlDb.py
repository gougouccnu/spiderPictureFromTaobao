# -*- coding: utf-8 -*-
#!/usr/bin/python3
import shelve
import logging
import sqlite3
# 实现__new__方法来实现单例类
#并在将一个类的实例绑定到类变量_instance上,
#如果cls._instance为None说明该类还没有实例化过,实例化该类,并返回
#如果cls._instance不为None,直接返回cls._instance

# pyton3 orig.__new__不能给参数了
# http://stackoverflow.com/questions/34777773/typeerror-object-takes-no-parameters-after-defining-new
class Singleton(object):
	def __new__(cls, *args, **kw):
		if not hasattr(cls, '_instance'):
			orig = super(Singleton, cls)
			cls._instance = orig.__new__(cls)
		return cls._instance

class itemUrlDb(Singleton):
	def __init__(self, dbName):
		super(itemUrlDb, self).__init__()
		self.conn = sqlite3.connect(dbName)
		self.c = self.conn.cursor()
		# TODO. has to see if create table
		#self.createTable()

	def createTable(self):
		self.c.execute('''CREATE TABLE lookMoreUrlTable (lookMoreUrl text)''')
		self.c.execute('''CREATE TABLE ItemUrlTable (ItemUrl text, isNew text)''')
		self.c.execute('''CREATE TABLE pictureUrlTable (pictureUrl text, isUpload text)''')

	def saveLookMoreUrl(self, lookMoreUrl):
		self.c.execute("INSERT INTO lookMoreUrlTable VALUES (?)", (lookMoreUrl,))
		self.conn.commit()

	def queryAllLookMoreUrl(self):
		self.c.execute("SELECT lookMoreUrl FROM lookMoreUrlTable")
		return self.c.fetchall()

	def addItem(self, itemUrl, isNew):
		self.c.execute("INSERT INTO ItemUrlTable VALUES (?, ?)", (itemUrl, isNew))
		self.conn.commit()

	def queryIfItemUrlSaved(self, itemUrl):
		self.c.execute("SELECT * FROM ItemUrlTable WHERE ItemUrl = '%s'" % itemUrl)
		#print(self.c.fetchone())
		if self.c.fetchone() == (itemUrl, 'saved'):
			return True
		else:
			return False

	def queryAllTodayItem(self):
		pass

	def queryIfPicUrlUpload(self, picUrl):
		self.c.execute("SELECT * FROM pictureUrlTable WHERE pictureUrl = '%s'" % picUrl)
		#print(self.c.fetchone())
		if self.c.fetchone() == (picUrl, 'upload'):
			return True
		else:
			return False

	def addPictureUrl(self, pictureUrl):
		self.c.execute("INSERT INTO pictureUrlTable VALUES (?, ?)", (pictureUrl, 'upload'))
		self.conn.commit()

	def queryAllPictureUrl(self):
		self.c.execute("SELECT * FROM pictureUrlTable")


	def deleteItem(self, itemUrl):
		self.c.execute("DELETE FROM ItemUrlTable WHERE ItemUrl = '%s'" % itemUrl)
		self.conn.commit()

	def queryAllItems(self):
		self.c.execute("SELECT itemUrl FROM ItemUrlTable")
		return self.c.fetchall()

	def close(self):
		self.conn.close()

if __name__ == "__main__":
	picUrl = 'https://gd1.alicdn.com/imgextra/i3/0/TB10lxmNVXXXXbiXFXXXXXXXXXX_!!0-item_pic.jpg_400x400.jpg'

	myDB = itemUrlDb()
	item = (picUrl, 'saved')
	myDB.addItem('ItemUrlTable', picUrl, 'saved')
	print(myDB.queryIfItemUrlSaved('ItemUrlTable', picUrl))