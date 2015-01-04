import sys
import MySQLdb
import hashlib
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from storescraper.items import StoreItem

import urlparse
class WholeFoodsSpider(Spider):
    name = "wholefoods"
    storestring = "WholeFoods"
    allowed_domains = ["wholefoodsmarket.com"]
    start_urls = []
    startUrl = "http://www.wholefoodsmarket.com/sales-flyer?store=85"
    
    def start_requests(self):

        return [Request(url=self.startUrl,
        callback=self.parse)]
    
    def parse(self, response):
        
        hxs = HtmlXPathSelector(response)
        rows = hxs.xpath("//div[contains(@class, 'brand-name')]/div/../..")
        
        items = []
        
        for row in rows:
            
            item = StoreItem()
            name1 = name2 = name = ""
            name1 = row.xpath("div[1]/div[1]/text()").extract()
            name2 = row.xpath("div[2]/div[1]/text()").extract()
            name = str(name1[0]) + " " + str(name2[0])
            print name
            item['name'] = name
            
            price1 = price2 = price = ""
            try:
                
                price1 = row.xpath("div[5]//div[contains(@class, 'sale_line')]/span[1]/text()").extract()
                price2 = row.xpath("div[5]//div[contains(@class, 'sale_line')]/span[2]/text()").extract()
                price = str(price1[0]) + " " + str(price2[0])
                print price
            except:
                price1 = row.xpath("div[5]//div[contains(@class, 'sale_line')]/text()").extract()
                price = str(price1[0])
                print price
                
            item['price'] = price
            item['unit'] = ""
            #item['desc'] = row.select('@recipename').extract()
            item['store'] = self.storestring
            item['imgLink'] = ""
            item['department'] = ""
            item['picData'] = ""
            
            items.append(item)
        return items
