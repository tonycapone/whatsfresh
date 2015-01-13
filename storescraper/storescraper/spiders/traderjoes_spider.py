# -*- coding: utf-8 -*-
# Spider template for sites like Aldi that require crawling. Works well for shoplocal type sites


from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from storescraper.items import StoreItem
from bs4 import BeautifulSoup
import re
import urlparse
import MySQLdb

class TraderJoesSpider(Spider):
    storestring = "Trader Joes" # used for sql searches and storing Ex: 'Aldi'
    name = "traderjoes"        # name used for scrapy engine Ex: 'aldi'
    allowed_domains = ["traderjoes.com"] # Ex: ["wholefoodsmarket.com"]
    start_urls = []
    startUrl = "http://www.traderjoes.com/FEARLESS-FLYER/" # Ex: "http://www.wholefoodsmarket.com/sales-flyer?store=85"
    baseUrl = "http://www.traderjoes.com/FEARLESS-FLYER/" # Ex: "http://weeklyads.aldi.us"
    ilistxpath = "//div[@class='body']" # the container for item listings. | Ex: //div[@class='article productthumbnail listing-thumbnail'
    catxpath = "//ul[@class='list']" # List of links to each item
    next = "" # Ex: "//div[@id='topitemnav']//li[@class='next']/a"
    def start_requests(self):

        return [Request(url=self.startUrl,
        callback=self.parseLinks)]
        

          
            
    def parse(self, response):
        soup = BeautifulSoup(response.body)
        department = response.meta['department']
        name = soup.find("h1", class_="lead").get_text()
        
        entries = soup.find_all("strong")

        print(name)
        for item in entries:
            item = item.get_text()
            if u'¢' in item or '$' in item:
                price = item

        imglink = "www.traderjoes.com" + soup.find("img", alt=name)["src"]
        storeitem = StoreItem()
            
        storeitem['name'] = name
        storeitem['price'] = price
        storeitem['unit'] = ""
        storeitem['department'] = department
        storeitem['store'] = self.storestring
        storeitem['imgLink'] = imglink
        storeitem['picData'] = ""




        return storeitem
        
    def parseCategory(self, response):
        soup = BeautifulSoup(response.body, "html5lib")
        links = soup.find_all("a", class_=re.compile("link4.*"))
        for link in links:
            request = Request("http://www.traderjoes.com" + link['href'])
            yield request
        
    def parseLinks(self, response):
        soup = BeautifulSoup(response.body, "html5lib")
        options = soup.find(text="Product categories").parent.parent.find_all("li")
        
        for option in options:
            url = "http://www.traderjoes.com/" + option.a['href']
            request = Request(url=url,callback=self.parseCategory)
            request.meta['department'] = option.get_text()
            yield request
             


