from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from storescraper.items import StoreItem
import MySQLdb
from bs4 import BeautifulSoup
import urlparse
import re


class ShopnsaveSpider(Spider):
    storestring = "ShopNSave"
    name = "shopnsave"
    allowed_domains = ["shopnsave.com"]
    start_urls = []
    def start_requests(self):
        
        return [Request(url="http://shopnsave.com/savings/view-ads/search-circular.html?keyword=&circularId=93728&sneakPeek=false&storeId=4542",
        callback=self.parseLinks)]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html5lib")
        department = response.meta['department']
        
        itemlist = soup.find_all("div", class_='special-inner')

        items = []
        
        for item in itemlist:
            name = item.find("h2").get_text().encode('ascii', 'ignore')
            price = item.find("p").span.get_text().encode('ascii', 'ignore')
            expiration = item.find("div", class_='expiration').get_text().encode('ascii', 'ignore')
            
            desc = item.find("span",class_='savings').get_text().encode('ascii', 'ignore')
            imglink = item.find("img")["src"].encode('ascii', 'ignore').split("http://")[1]
            storeitem = StoreItem()
            storeitem['name'] = name
            storeitem['price'] = price
            storeitem['unit'] = ""
            #storeitem['expiration'] = expiration
            storeitem['desc'] = desc
            storeitem['department'] = department
            storeitem['store'] = self.storestring
            storeitem['imgLink'] = imglink
            items.append(storeitem)

        return items

    def parseLinks(self, response):
        hxs = Selector(response)
        options = hxs.xpath("//select[@id='category']/option")

        
        for option in options:
            departments = option.xpath("text()").extract()[0]
            
            print(departments)
            
            depID = option.xpath("@value").extract()
            depID = str(depID[0])
            
            depUrl = "http://shopnsave.com/savings/view-ads/search-circular.html?category=%s&displayCount=500" % depID

            

            request = Request(url=depUrl)
            request.meta['department'] = departments
            yield request




