import sys
import MySQLdb
import hashlib
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from storescraper.items import StoreItem

import urlparse
class TraderJoesSpider(Spider):
    name = "traderjoes"
    storestring = "Trader Joes"
    allowed_domains = ["http://stlouis.findnsave.com/"]
    start_urls = []
    startUrl = "http://stlouis.findnsave.com/store/Trader-Joes/10272/"
    
    def start_requests(self):

        return [Request(url=self.startUrl,
        callback=self.parse)]
    
    def parse(self, response):
        
        hxs = HtmlXPathSelector(response)
        rows = hxs.xpath("//section[@id='content']/ul/li[contains(@id, 'offer')]")
        
        items = []
        
        for row in rows:
            
            item = StoreItem()
            name = row.xpath("h3/a/text()").extract()
            
            name = str(name[0])
            print name
            item['name'] = name
            
            price = row.xpath("div[@class='product-price']/span/text()").extract()
            
                
            item['price'] = price
            
            #item['desc'] = row.select('@recipename').extract()
            item['store'] = self.storestring
           
            item['department'] = ""
            
            items.append(item)
        return items
