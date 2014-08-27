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
        self.conn = MySQLdb.connect(user='root', passwd='tidesof', db='storeapp', host='localhost', charset="utf8", use_unicode=True)
        
        return [Request(url="http://exposhopper.p2ionline.com/Dierbergs/sitebase/index.aspx?area=singlepage&adgroupid=225279&pagenumber=1",
        callback=self.getPages)]
    
    def parse(self, response):
        soup = BeautifulSoup(response.body)
        areaTagList = soup.find(id="StoryMap").find_all("area")
        items = []
        import pdb; pdb.set_trace()
        for areaTag in areaTagList:
            innerSoup = BeautifulSoup(areaTag['onmouseover'].replace("Tip('", "").replace("')",""))
            item = StoreItem()
            item['price'] = innerSoup.find(class_="headersub").get_text()
            print item['price']
            
            import pdb; pdb.set_trace()
           # item['unit'] = ""
            #item['name'] = site.select('@ingredient').extract()
           # item['desc'] = site.select('@recipename').extract()
            #item['store'] = 'Schnucks'
           # item['department'] = site.select('@department').extract()
           # item['imglink'] = site.select('@coords').extract()
            
           # items.append(item)
        return items
    def getPages(self, response):
        soup = BeautifulSoup(response.body)
        
        totalPages = soup.find(class_="white_bar").get_text().split(" of ")[1]
        for x in range(1,int(totalPages)):
            nexturl = "http://exposhopper.p2ionline.com/Dierbergs/sitebase/index.aspx?area=singlepage&adgroupid=225279&pagenumber=" + str(x)
            
            request = Request(url=nexturl)
            yield request
        