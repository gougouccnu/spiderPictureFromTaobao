# -*- coding: utf-8 -*-
import shelve

# 实现__new__方法来实现单例类
#并在将一个类的实例绑定到类变量_instance上,
#如果cls._instance为None说明该类还没有实例化过,实例化该类,并返回
#如果cls._instance不为None,直接返回cls._instance
class Singleton(object):
	def __new__(cls, *args, **kw):
		if not hasattr(cls, '_instance'):
			orig = super(Singleton, cls)
			cls._instance = orig.__new__(cls, *args, **kw)
		return cls._instance


class Rules(Singleton):
	def __init__(self, filename):
		super(Rules, self).__init__()
		self.filename = filename
		self.d = shelve.open(self.filename)

	def saveRule(self, key, value):
		# if self.d.has_key(key):
		# 	print('save Error:key ' + key + ' exist!')
		# else:
		self.d[key] = value

	def loadValue(self, key):
		#list(self.d.keys())
		if key in self.d:
		#if self.d.has_key(key):
			value = self.d[key]
			return value
		else:
			print('load Error:key ' + key + ' don\'t exist')
			return None

	def close(self):
		self.d.close()

	def deleteElement(self, key):
		del self.d[key]

if __name__ == "__main__":
	picUrl = 'https://gd1.alicdn.com/imgextra/i3/0/TB10lxmNVXXXXbiXFXXXXXXXXXX_!!0-item_pic.jpg_400x400.jpg'

	rules = Rules()
	rules.saveRule(picUrl, 'saved')
	print(rules.loadValue(picUrl))
