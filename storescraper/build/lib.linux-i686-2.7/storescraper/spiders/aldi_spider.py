from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from storescraper.items import StoreItem
import urlparse
import MySQLdb

class AldiSpider(BaseSpider):
    storestring = "Aldi"
    name = "aldi"
    allowed_domains = ["aldi.us"]
    start_urls = []
    def start_requests(self):
        self.conn = MySQLdb.connect(user='root', passwd='tidesof', db='stores', host='localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""DELETE from store WHERE store = 'Aldi'""")
        self.conn.commit()
        
        
        return [Request(url="http://weeklyads.aldi.us/aldi/default.aspx?action=entry&pretailerid=-97994&siteid=1337&mode=html&StoreID=2624123",
        callback=self.parseLinks)]
        
    def parseItems(self, hxs, department):
        itemlist = hxs.xpath("//div[@class='article productthumbnail listing-thumbnail']")
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
            storeitem['store'] = 'Aldi'
            
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
        
		
        nav = hxs.xpath("//div[@id='topitemnav']//li[@class='next']/a")
        moreItems = self.parseItems(hxs, department)
        items.extend(moreItems)
        try:
            relUrl = str(nav.xpath("@href").extract()[0])
            
        except:
            return items
        
        else:
            nextUrl = urlparse.urljoin('http://weeklyads.aldi.us', relUrl)
            
            
            
            request = Request(url=nextUrl)
            request.meta['department'] = department
            request.meta['items'] = items
            return request
        
    def parseLinks(self, response):
        hxs = Selector(response)
        options = hxs.xpath("//ul[@id='categorylist']/li/a")
        
        
        for option in options:
            relUrl = str(option.xpath("@href").extract()[0])
            
            depUrl = urlparse.urljoin('http://weeklyads.aldi.us', relUrl)
            departments = option.xpath("text()").extract()
            print(depUrl)
            print(departments)
            
            request = Request(url=depUrl)
            request.meta['department'] = departments
            yield request
             


