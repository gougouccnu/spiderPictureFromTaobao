# -*- coding: utf8 -*-
#!/usr/bin/python
import urllib
import urllib2
import json,httplib

def postToBmob(url, table, data):
    urls = url + '/' + table
    data = json.dumps(data)
    headers = {"X-Bmob-Application-Id": "b78b5e674bac32a880a7b65c36531534",
              "X-Bmob-REST-API-Key": "386d24d4a17d00e09208c8f3ddc1a17e",
              "Content-Type": "application/json"
              }
    req = urllib2.Request(urls, data, headers)
    response = urllib2.urlopen(req)
    print response.read()
    

def getFromBmob(url, table, objectId):
    urls = url + '/' + table + '/' + objectId
    headers = {"X-Bmob-Application-Id": "b78b5e674bac32a880a7b65c36531534",
              "X-Bmob-REST-API-Key": "386d24d4a17d00e09208c8f3ddc1a17e"}
    req = urllib2.Request(urls, None, headers)
    response = urllib2.urlopen(req)
    print response.read()

if __name__ == "__main__":

    url = 'https://api.bmob.cn/1/classes'

    getFromBmob(url, 'picInf', 'N0Kl888I')

    data = {
        "picUrl":"https://gd1.alicdn.com/imgextra/i3/0/TB10lxmNVXXXXbiXFXXXXXXXXXX_!!0-item_pic.jpg_400x400.jpg", 
        "itemUrl":"https://item.taobao.com/item.htm?id=539503242702", 
        "starter":{"__type":"Pointer","className":"_User","objectId":"JLkR444G"
        }
    }
    
    postToBmob(url, 'picInf', data)
    # import requests

    # response = requests.get('https://api.bmob.cn/1/classes/picInf/N0Kl888I',
    #                      auth=("X-Bmob-Application-Id": "b78b5e674bac32a880a7b65c36531534",
    #           "X-Bmob-REST-API-Key": "386d24d4a17d00e09208c8f3ddc1a17e")
    # data = response.json()
    # # print(data)
    # urls = 'https://api.parse.com'
    # connection = httplib.HTTPSConnection(urls, 80)
    # connection.connect()
    # connection.request('GET', '/1/classes/picInf', {"X-Bmob-Application-Id": "b78b5e674bac32a880a7b65c36531534",
    #           "X-Bmob-REST-API-Key": "386d24d4a17d00e09208c8f3ddc1a17e"})
    # result = json.loads(connection.getresponse().read())
    # print result