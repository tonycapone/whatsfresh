import sys
import MySQLdb
import hashlib
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from storescraper.items import StoreItem

import urlparse
class SchnucksSpider(Spider):
    name = "schnucks"
    storestring = "Schnucks"
    allowed_domains = ["schnucks.shoptocook.com"]
    start_urls = []
    
    def start_requests(self):

        return [Request(url="http://schnucks.shoptocook.com/weeklyad.jsp?circularstoreidentifier=WHL1KQNZBR3ML1AKR10JYOVFWKCOFC6YBBJPMD",
        callback=self.parse)]
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@id="mainbody"]/map/area')
        items = []
        for site in sites:
            item = StoreItem()
            item['price'] = site.select('@deal').extract()[0]
            item['unit'] = ""
            item['name'] = site.select('@ingredient').extract()[0]
            item['desc'] = site.select('@recipename').extract()[0]
            item['store'] = 'Schnucks'
            item['department'] = site.select('@department').extract()[0]
            item['picData'] = site.select('@coords').extract()
            item['imgLink'] = site.select('../@name').extract()[0]
	    items.append(item)
        return items
