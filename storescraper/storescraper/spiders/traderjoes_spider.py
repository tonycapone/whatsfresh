# -*- coding: utf-8 -*-
# Spider template for sites like Aldi that require crawling. Works well for shoplocal type sites


from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from storescraper.items import StoreItem
from bs4 import BeautifulSoup
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
        hxs = Selector(response)
        soup = BeautifulSoup(response.body)
        body = hxs.xpath(self.ilistxpath)
        items = []
        department = response.meta['department']
        name = response.meta['name'] #pull name from sidebar
        
        entries = body.xpath('//strong/text()').extract()
        #name = entries[0] #pull name from first entry
        print(name)
        for item in entries:
            
            if u'¢' in item or '$' in item:
                price = item
                
            else:
                price = "no price"
            print price.encode('ascii', 'ignore')
        imglink = "www.traderjoes.com" + soup.find("img", alt=name)["src"]
        storeitem = StoreItem()
            
        storeitem['name'] = name[0]
        storeitem['price'] = price
        storeitem['unit'] = ""
        #storeitem['expiration'] = expiration
        #storeitem['desc'] = desc
        storeitem['department'] = department[0]
        storeitem['store'] = self.storestring
        storeitem['imgLink'] = imglink
        storeitem['picData'] = ""

        items.append(storeitem)
        
        
        
        
        
        return items
        
       
        
    def parseLinks(self, response):
        hxs = Selector(response)
        options = hxs.xpath(self.catxpath)
        
        
        for option in options:
            itemname = option.xpath("a/text()").extract()
            relUrl = option.xpath("a/@href").extract()
            relUrl = str(relUrl[0])
            
            
            itemUrl = self.baseUrl + relUrl
            department = option.xpath("../../div[@class='category-header']/h3/text()").extract()
            
                      
            request = Request(url=itemUrl)
            request.meta['department'] = department
            request.meta['name'] = itemname
            yield request
             


