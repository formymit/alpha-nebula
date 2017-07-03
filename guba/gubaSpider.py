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

url = 'http://guba.eastmoney.com/'

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

        all_reads = selector.xpath('//ul[@class="newlist"]/li/cite[1]/text()')
        all_comments = selector.xpath('//ul[@class="newlist"]/li/cite[2]/text()')
        all_balinks = selector.xpath('//span[@class="sub"]/a[@class="balink"]/text()')
        all_titles = selector.xpath('//span[@class="sub"]/a/@title')
        all_title_hrefs = selector.xpath('//span[@class="sub"]/a[@class="note"]/@href')
        all_authors = selector.xpath('//ul[@class="newlist"]/li/cite[3]/a/text()')
        all_post_dates = selector.xpath('//ul[@class="newlist"]/li/cite[4]/text()')
        all_last_date = selector.xpath('//ul[@class="newlist"]/li/cite[4]/text()')

        for i in range(len(all_reads)):
            read = all_reads[i]
            comment = all_comments[i]
            balink = all_balinks[i]
            title = all_titles[i]
            title_href = 'http://guba.eastmoney.com' + all_title_hrefs[i]
            author = all_authors[i]
            post_date = all_post_dates[i]
            last_date = all_last_date[i]
            print(read + '\t' + comment + '\t' + balink + '\t' + title + '\t' +title_href + '\t' + author + '\t' + post_date + '\t' + last_date)
    except Exception as e:
        print(e)
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
    process_crawler()

