from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector

from ..items import StoreItem
from bs4 import BeautifulSoup
import urlparse
import re

class AldiSpider(Spider):
    storestring = "Aldi"
    name = "aldi"
    allowed_domains = ["aldi.us"]
    start_urls = []
    
    def start_requests(self):
        
        return [Request(url="http://weeklyads.aldi.us/Aldi/BrowseByListing/ByAllListings/?StoreID=2624123#PageNumber=1",
        callback=self.parseLinks)]
        
    def parse(self, response):
        soup = BeautifulSoup(response.body, "html5lib")

        items = response.meta['items']
        itemGridPage = soup.find(class_="gridpage")
        if itemGridPage is None:
            return items
        else:
            itemlist = itemGridPage.find_all(class_="gridTileInfo")
        for item in itemlist:
            storeitem = StoreItem()
            try:
                name = item.find(class_="action-goto-listingdetail").get_text().encode('ascii', 'ignore').strip()
                price = item.find(class_="deal").get_text().encode('ascii', 'ignore')

            except:
                print("no name or price found")


            unit = item.find(class_="priceQualifier")
            if unit is not None:
                unitText = unit.get_text().encode('ascii', 'ignore').strip()
            else:
                unitText = ""
            imglink = item.parent.find('img')['style'].split("//")[1].split(");")[0]

            storeitem['name'] = name
            storeitem['price'] = price
            storeitem['unit'] = unitText
            storeitem['department'] = response.meta['department']
            storeitem['store'] = 'Aldi'
            storeitem['imgLink'] = imglink
            storeitem['picData'] = ""

            items.append(storeitem)
        nextButton = soup.find("a", class_=("skinPaddleRight inactive action-nextpage action-tracking-nav gutterPositionRight"))
        if "javascript:void(0)" in nextButton['href']:
            print "no more items"
            return items

        else:

            print "more items"
            nextUrl = urlparse.urljoin('http://weeklyads.aldi.us', nextButton['href'])
            print "nexturl:" + nextUrl


            request = Request(url=nextUrl)
            request.meta['department'] = response.meta['department']
            request.meta['items'] = items
            return request


          
            
    """def parse(self, response):

        soup = BeautifulSoup(response.body, "html5lib")
        items = []

        try:
			items = response.meta['items']
        except:
            print('No items yet')

        print(response.url)
        moreItems = self.parseItems(response, department)
        items.extend(moreItems)

        nextButton = soup.find("a", class_=("skinPaddleRight inactive action-nextpage action-tracking-nav gutterPositionRight"))
        if "javascript:void(0)" in nextButton['href']:
            print "no more items"
            return items

        else:

            print "more items"
            nextUrl = urlparse.urljoin('http://weeklyads.aldi.us', nextButton['href'])
            print "nexturl:" + nextUrl
                """

        
    def parseLinks(self, response):
        soup = BeautifulSoup(response.body, "html5lib")
        options = soup.find(id='IScrollHeaderCatContent').find_all("a", href=re.compile("ByCategory"))    
        
        for option in options:
            relUrl = option['href']
            
            depUrl = urlparse.urljoin('http://weeklyads.aldi.us', relUrl)
            departments = option.get_text().encode('ascii', 'ignore').strip()
            
            request = Request(url=depUrl)
            request.meta['department'] = departments
            request.meta['items'] = []
            yield request
             


