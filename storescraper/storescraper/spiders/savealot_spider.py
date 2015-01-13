from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from storescraper.items import StoreItem
from bs4 import BeautifulSoup
import re

class SaveALotSpider(Spider):
    storestring = "Save A Lot" # used for sql searches and storing
    name = "savealot"
    allowed_domains = ["savealot.shoplocal.com"] # Ex: ["wholefoodsmarket.com"]
    start_urls = []
    startUrl = "http://savealot.shoplocal.com/SaveALot/Entry/LandingContent?storeid=2655389" # Ex: "http://www.wholefoodsmarket.com/sales-flyer?store=85"
    baseUrl = "http://savealot.shoplocal.com/" 
    
    def start_requests(self):
        
        return [Request(url=self.startUrl,
        callback=self.parseLinks)]
        
    def parse(self, response):
        soup = BeautifulSoup(response.body, "html5lib")
        department = response.meta['department']
        items = response.meta['items']
        itemlist =  soup.find_all(class_='gridTileContain')


        for item in itemlist:
            storeitem = StoreItem()
            name = item.find('div', class_='gridTileUnitB').a.span.get_text().encode('ascii', 'ignore')
            
            price = item.find('div', class_='deal action-elide').find(class_='ellipsis_text').get_text().encode('ascii', 'ignore')
            
            try:
                imglink = item.find(class_='image cursorPointer')['style'].encode('ascii', 'ignore')
                imglink = re.search('akimages(.*).jpg', imglink).group(0)
            except:
                imglink = "No Image"
            #desc = item.xpath("").extract()
        
            
            storeitem['name'] = name
            storeitem['price'] = price
            storeitem['unit'] = ""
            storeitem['department'] = department
            storeitem['store'] = self.storestring
            storeitem['imgLink'] = imglink
            storeitem['picData'] = ""
            
            items.append(storeitem)
         # if response contains more data, parse the items
        if "There is no content for this page." not in response.body:
            depId = response.meta['depId']
            depIndex = response.meta['depIndex']
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
            request.meta['items'] = []
            yield request
             


