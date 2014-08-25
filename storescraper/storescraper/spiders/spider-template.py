# Spider template for sites like Aldi that require crawling. Works well for shoplocal type sites
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from storescraper.items import StoreItem
import urlparse
import MySQLdb

class ExampleSpider(Spider):
    storestring = "" # used for sql searches and storing Ex: 'Aldi'
    name = ""        # name used for scrapy engine Ex: 'aldi'
    allowed_domains = [""] # Ex: ["wholefoodsmarket.com"]
    start_urls = []
    startUrl = "" # Ex: "http://www.wholefoodsmarket.com/sales-flyer?store=85"
    baseUrl = "" # Ex: "http://weeklyads.aldi.us"
    ilistxpath = "" # the container for item listings. | Ex: //div[@class='article productthumbnail listing-thumbnail'
    catxpath = "" # List of links to each category Ex: "//ul[@id='categorylist']/li/a"
    next = "" # Ex: "//div[@id='topitemnav']//li[@class='next']/a"
    def start_requests(self):
        
        
        return [Request(url=self.startUrl,
        callback=self.parseLinks)]
        
    def parseItems(self, hxs, department):
        itemlist = hxs.xpath(ilistxpath)
        items = []    
        for item in itemlist:
            storeitem = StoreItem()
            name = item.xpath("h5[@class='title']/a/@title").extract()
            print(name)
            price = item.xpath("div[@class='infocontainer']/ul/li[@class='deal']/text()").extract()
            desc = item.xpath("div[@class='infocontainer']/ul/li[@class='additionaldealinfo']/text()").extract()
        
            
            storeitem['name'] = name
            storeitem['price'] = price
            #storeitem['expiration'] = expiration
            storeitem['desc'] = desc
            storeitem['department'] = department
            storeitem['store'] = self.storestring
            
            items.append(storeitem)
    
        return items
          
            
    def parse(self, response):
        
        hxs = Selector(response)
        items = []
        department = response.meta['department']
        try:
			items = response.meta['items']
        except:
            print('No items yet')
			
        print(response.url)
        
		
        nav = hxs.xpath(self.next) # get the 'next' link
        moreItems = self.parseItems(hxs, department)
        items.extend(moreItems)
        try:
            relUrl = str(nav.xpath("@href").extract()[0])
            
        except:
            return items
        
        else:
            nextUrl = urlparse.urljoin('self.baseUrl', relUrl)
            
            
            
            request = Request(url=nextUrl)
            request.meta['department'] = department
            request.meta['items'] = items
            return request
        
    def parseLinks(self, response):
        hxs = Selector(response)
        options = hxs.xpath(self.catxpath)
        
        
        for option in options:
            relUrl = str(option.xpath("@href").extract()[0])
            
            depUrl = urlparse.urljoin(self.baseUrl, relUrl)
            departments = option.xpath("text()").extract()
            print(depUrl)
            print(departments)
            
            request = Request(url=depUrl)
            request.meta['department'] = departments
            yield request
             


