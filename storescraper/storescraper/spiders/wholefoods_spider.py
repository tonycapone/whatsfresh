import sys
import MySQLdb
import hashlib
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import HtmlXPathSelector
from storescraper.items import StoreItem
from bs4 import BeautifulSoup

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
        
        soup = BeautifulSoup(response.body, "html5lib")
        rows = soup.find_all("div", class_="views-row views-row-odd")
        
        items = []
        
        for row in rows:
            
            item = StoreItem()
            name1 = name2 = name = ""
            name1 = row.find("div", class_="views-field views-field-field-flyer-brand-name").get_text()
            name2 = row.find("div", class_="views-field views-field-field-flyer-product-name").get_text()
            name = name1 + " " + name2
            print name
            priceDiv = row.find("div", class_="sale_line")
            if priceDiv.find("span", class_="my_price") is not None:
                price = priceDiv.find("span", class_="my_price").get_text()
                unit = priceDiv.find("span", class_="sub_price").get_text()
            else:
                price = priceDiv.get_text()
            item['name'] = name
            item['price'] = price
            item['unit'] = unit
            item['store'] = self.storestring
            item['imgLink'] = ""
            item['department'] = ""
            item['picData'] = ""
            
            items.append(item)
        return items
