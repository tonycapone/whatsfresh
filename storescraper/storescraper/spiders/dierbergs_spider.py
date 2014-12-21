# -*- coding: utf-8 -*-
import sys
import MySQLdb
import hashlib
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from storescraper.items import StoreItem
from bs4 import BeautifulSoup
import re

import urlparse
class DierbergsSpider(Spider):
    name = "dierbergs"
    storestring = "Dierbergs"
    #allowed_domains = ["http://exposhopper.p2ionline.com"]
    start_urls = []
    
    def start_requests(self):

        
        return [Request(url="http://exposhopper.p2ionline.com/Dierbergs/sitebase/index.aspx?area=singlepage&adgroupid=225279&pagenumber=1",
        callback=self.getPages)]
    
    def parse(self, response):
        soup = BeautifulSoup(response.body)
        areaTagList = soup.find(id="StoryMap").find_all("area")
        items = []
        
        for areaTag in areaTagList:
            innerSoup = BeautifulSoup(areaTag['onmouseover'].replace("Tip('", "").replace("')",""))
            item = StoreItem()
            name = innerSoup.find(class_="headersub").get_text()
            print name.encode("ascii", "ignore")
            
            for x in innerSoup.find_all(class_="add_caption3"):
                if u'¢' in x.get_text() or '$' in x.get_text():
                    price = x.get_text()
            
            
            item['name'] = name
            item['unit'] = ""
            item['price'] = price
            item['department'] = ""
           # item['desc'] = site.select('@recipename').extract()
            item['store'] = 'Dierbergs'
            item['imglink'] = ""
            
            items.append(item)
        return items
    def getPages(self, response):
        soup = BeautifulSoup(response.body)
        
        totalPages = soup.find(class_="white_bar").get_text().split("/")[1]
        for x in range(1,int(totalPages)):
            nexturl = "http://exposhopper.p2ionline.com/Dierbergs/sitebase/index.aspx?area=singlepage&adgroupid=225279&pagenumber=" + str(x)
            
            request = Request(url=nexturl)
            yield request
        