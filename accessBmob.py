# -*- coding: utf8 -*-
#!/usr/bin/python
import urllib.request
#import urllib2
import json
import urllib.parse
from urllib.error import URLError, HTTPError 

def postToBmob(url, table, data):
    urls = url + '/' + table
    #value = json.dumps(data)
    jdata = json.dumps(data)
    print(data)
    value = urllib.parse.urlencode(data, safe=':'+'/') 
    print("value is: " + value)
    binary_data = value.encode('ascii')
    headers = {
              "X-Bmob-Application-Id": "b78b5e674bac32a880a7b65c36531534",
              "X-Bmob-REST-API-Key": "386d24d4a17d00e09208c8f3ddc1a17e",
              "Content-Type": "application/json"
            }
    print(binary_data)
    req = urllib.request.Request(urls, binary_data, headers)
    print(req.full_url)
    try:
        response = urllib.request.urlopen(req)
    except HTTPError as e:
        print('***')
        print(e.geturl())
        print(e.info())
        print(e.code)
        #print(e.read().decode('ascii'))
        print(e.read())
    except URLError as e:
        print(e.reason)
    else:
        pass

def getFromBmob(url, table, objectId):
    urls = url + '/' + table + '/' + objectId
    headers = {"X-Bmob-Application-Id": "b78b5e674bac32a880a7b65c36531534",
              "X-Bmob-REST-API-Key": "386d24d4a17d00e09208c8f3ddc1a17e"}
    req = urllib.request.Request(urls, None, headers)
    print('request full url: ' + req.full_url)
    response = urllib.request.urlopen(req)
    print(response.read())
    print('****')
    print(response.geturl())
    print(response.info())

if __name__ == "__main__":

    url = 'https://api.bmob.cn/1/classes'

    # getFromBmob(url, 'picInf', 'N0Kl888I')

    # data = {"picUrl":"https://gd1.alicdn.com/imgextra/i3/0/TB10lxmNVXXXXbiXFXXXXXXXXXX_!!0-item_pic.jpg_400x400.jpg"}
    # data1 = {
    #     "picUrl":"https://gd1.alicdn.com/imgextra/i3/0/TB10lxmNVXXXXbiXFXXXXXXXXXX_!!0-item_pic.jpg_400x400.jpg", 
    #     "itemUrl":"https://item.taobao.com/item.htm?id=539503242702", 
    #     "starter":{"__type":"Pointer","className":"_User","objectId":"JLkR444G"},
    #     "user":{"__type":"Pointer","className":"_User","objectId":"JLkR444G"}
    # }

    # postToBmob(url, 'picInf', data)
    # import requests

    # response = requests.get('https://api.bmob.cn/1/classes/picInf/N0Kl888I',
    #                      auth=("X-Bmob-Application-Id": "b78b5e674bac32a880a7b65c36531534",
    #           "X-Bmob-REST-API-Key": "386d24d4a17d00e09208c8f3ddc1a17e")
    # data = response.json()
    # # print(data)
    #urls = 'https://api.parse.com'
    import http
    connection = http.client.HTTPSConnection('api.bmob.cn')
    connection.connect()
    connection.request('POST', '/1/classes/picInf', 
        json.dumps({"picUrl":"https://gd1.alicdn.com/imgextra/i3/0/TB10lxmNVXXXXbiXFXXXXXXXXXX_!!0-item_pic.jpg_400x400.jpg"}),
        {"X-Bmob-Application-Id": "b78b5e674bac32a880a7b65c36531534",
              "X-Bmob-REST-API-Key": "386d24d4a17d00e09208c8f3ddc1a17e",
              "Content-Type": "application/json"})
    result = connection.getresponse().read().decode()
    print(json.loads(result)['objectId'])