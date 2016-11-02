# -*- coding: utf8 -*-
#!/usr/bin/python

import http.client
import json

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

def postToBmob(url, table, data):
    connection = http.client.HTTPSConnection(url)
    connection.connect()
    connection.request('POST', '/1/classes' + '/' + table, data,
            {"X-Bmob-Application-Id": "b78b5e674bac32a880a7b65c36531534",
              "X-Bmob-REST-API-Key": "386d24d4a17d00e09208c8f3ddc1a17e",
              "Content-Type": "application/json"})
    result = connection.getresponse().read().decode()
    print('POST DATA TO BMOB INFO: ' + result)
    # TODO:check if post data success

if __name__ == "__main__":

    url = 'api.bmob.cn'
    table = 'picInf'
    newPic = {"picUrl":"https://gd1.alicdn.com/imgextra/i3/0/TB10lxmNVXXXXbiXFXXXXXXXXXX_!!0-item_pic.jpg_400x400.jpg"}
    data = json.dumps(newPic)

    postToBmob(url, table, data)

    # connection = http.client.HTTPSConnection('api.bmob.cn')
    # connection.connect()
    # connection.request('POST', '/1/classes/picInf', 
    #     json.dumps({"picUrl":"https://gd1.alicdn.com/imgextra/i3/0/TB10lxmNVXXXXbiXFXXXXXXXXXX_!!0-item_pic.jpg_400x400.jpg"}),
    #     {"X-Bmob-Application-Id": "b78b5e674bac32a880a7b65c36531534",
    #           "X-Bmob-REST-API-Key": "386d24d4a17d00e09208c8f3ddc1a17e",
    #           "Content-Type": "application/json"})
    # result = connection.getresponse().read().decode()
    # print(json.loads(result)['objectId'])