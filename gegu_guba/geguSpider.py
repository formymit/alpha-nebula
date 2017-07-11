#!usr/bin/env python3.6  
#-*- coding:utf-8 -*-  
""" 
@author:iBoy 
@file: gubaSpider.py
@time: 2017/07/03
"""
import requests
from lxml import etree
import time
from mongodb_queue import MongoQueue
import multiprocessing
import traceback
url = 'http://guba.eastmoney.com/remenba.aspx?type=1'
# url = 'http://guba.eastmoney.comlist,300104.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0',
}

spider_queue = MongoQueue('guba', 'page_urls')

def startWork():
    while True:
        try:
            url = spider_queue.pop()
            print(url)
        except KeyError:
            print('No Data...')
            break
        else:
            status_code = getdata(url)
            if status_code == 200:
                spider_queue.complete(url)
            else:
                spider_queue.reset(url)


def getdata(url):
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        selector = etree.HTML(response.text)

        all_titles = selector.xpath('//ul[@class="ngblistul2"]//li//a//text()')
        all_hrefs = selector.xpath('//ul[@class="ngblistul2"]//li//a//@href')

        for i in range(len(all_titles)):
            title = all_titles[i]

            href = all_hrefs[i]


            if href[:4] != 'http' and href[0] != '/':
                href = 'http://guba.eastmoney.com/' + href
            elif href[:4] != 'http':
                href = 'http://guba.eastmoney.com' + href

            data = title + '\t' + href
            print(data)
            with open('gegu_list.txt', 'a') as f:
                f.write(data + '\n')


    except Exception as e:
        print(e)
        traceback.print_exc()
    return response.status_code

def process_crawler():
    process = []
    for i in range(10):
        p = multiprocessing.Process(target=startWork)
        p.start()
        process.append(p)
    for p in process:
        p.join()

if __name__ == '__main__':
    # process_crawler()
    getdata(url)
