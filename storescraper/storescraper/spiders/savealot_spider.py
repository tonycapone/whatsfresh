from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from storescraper.items import StoreItem
import urlparse
from bs4 import BeautifulSoup
import re
import MySQLdb

class ExampleSpider(Spider):
    storestring = "Save A Lot" # used for sql searches and storing
    name = "savealot"
    allowed_domains = ["savealot.shoplocal.com"] # Ex: ["wholefoodsmarket.com"]
    start_urls = []
    startUrl = "http://savealot.shoplocal.com/SaveALot/Entry/LandingContent?storeid=2655389" # Ex: "http://www.wholefoodsmarket.com/sales-flyer?store=85"
    baseUrl = "http://savealot.shoplocal.com/" 
    
    def start_requests(self):
        self.conn = MySQLdb.connect(user='root', passwd='tidesof', db='stores', host='localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""DELETE from store WHERE store = %s""", (self.storestring,))
        self.conn.commit()
        
        
        return [Request(url=self.startUrl,
        callback=self.parseLinks)]
        
    def parseItems(self, response, department):
        soup = BeautifulSoup(response.body, "html5lib")
        
        itemlist =  soup.find_all(class_='gridTileContain')
        items = []
        #import pdb; pdb.set_trace()
        for item in itemlist:
            storeitem = StoreItem()
            name = item.find('div', class_='gridTileUnitB').a.span.get_text().encode('ascii', 'ignore')
            print(name)
            
            price = item.find('div', class_='deal action-elide').find(class_='ellipsis_text').get_text().encode('ascii', 'ignore')
            print(price)
            
            try:
                imglink = item.find(class_='image cursorPointer')['style'].encode('ascii', 'ignore')
                imglink = re.search('akimages(.*).jpg', imglink).group(0)
            except:
                imglink = "No Image"
            #desc = item.xpath("").extract()
        
            
            storeitem['name'] = name
            storeitem['price'] = price
            #storeitem['expiration'] = expiration
            #storeitem['desc'] = desc
            storeitem['unit'] = ""
            storeitem['department'] = department
            storeitem['store'] = self.storestring
            storeitem['imglink'] = imglink
            
            items.append(storeitem)
    
        return items
          
            
    def parse(self, response):
        
        soup = BeautifulSoup(response.body, "html5lib")
        items = []
        department = response.meta['department']
        depId = response.meta['depId']
        depIndex = response.meta['depIndex']
        
        # get already scraped items
        try:
			items = response.meta['items']
        except:
            print('No items yet')
        
        # if response contains more data, parse the items
        if "There is no content for this page." not in response.body:
            moreItems = self.parseItems(response, department)
            items.extend(moreItems)
            depIndex = depIndex + 1
            # Then generate next url and request
            nextUrl = "http://savealot.shoplocal.com/SaveALot/BrowseByListing/ByCategory/?IsPartial=Y&ListingSort=23&StoreID=2655389&CategoryID=%s&PageNumber=%d"% (depId, depIndex)
            print "nextUrl: " + nextUrl
            
            request = Request(url=nextUrl)
            request.meta['depId'] = depId
            request.meta['depIndex'] = depIndex
            request.meta['department'] = department
            request.meta['items'] = items
            return request
        # else we've scraped all items for this department, so return scraped items
        else:
            return items
        
    def parseLinks(self, response):
        soup = BeautifulSoup(response.body, "html5lib")
        
        categories = soup.find("div", id='IScrollHeaderCatContent').find_all("a", class_="globalNavScrollLink")
        
        for category in categories:
            department = category.get_text().encode('ascii', 'ignore').strip()
            depId = category['href'].split("CategoryID=")[1]
            
            depUrl = "http://savealot.shoplocal.com/SaveALot/BrowseByListing/ByCategory/?IsPartial=Y&ListingSort=23&StoreID=2655389&CategoryID=%s&PageNumber=1"% depId
            
            print(department)
            print(depUrl)
            
            request = Request(url=depUrl)
            request.meta['department'] = department
            request.meta['depId'] = depId
            request.meta['depIndex'] = 1
            yield request
             

