from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from storescraper.items import StoreItem
import MySQLdb


class ShopnsaveSpider(BaseSpider):
    storestring = "ShopNSave"
    name = "shopnsave"
    allowed_domains = ["shopnsave.com"]
    start_urls = []
    def start_requests(self):
        self.conn = MySQLdb.connect(user='root', passwd='tidesof', db='stores', host='localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""DELETE from store WHERE store = 'ShopNSave'""")
        self.conn.commit()
        
        return [Request(url="http://shopnsave.com/savings/view-ads/search-circular.html?keyword=&circularId=93728&sneakPeek=false&storeId=4542",
        callback=self.parseLinks)]

    def parse(self, response):
        hxs = Selector(response)
        department = response.meta['department']

        itemlist = hxs.xpath("//div[@id='specials-list']//h2")

        items = []
        
        for item in itemlist:
            name = item.xpath("a/text()").extract()
            price = item.xpath("following-sibling::p[1]/span/text()").extract()
            expiration = item.xpath("following-sibling::div[@class='expiration']/text()").extract()
            desc = item.xpath("following-sibling::span[@class='savings']/text()").extract()

            storeitem = StoreItem()
            storeitem['name'] = name
            storeitem['price'] = price
            #storeitem['expiration'] = expiration
            storeitem['desc'] = desc
            storeitem['department'] = department
            storeitem['store'] = self.storestring

            items.append(storeitem)

        return items

    def parseLinks(self, response):
        hxs = Selector(response)
        options = hxs.xpath("//select[@id='category']/option")


        for option in options:
            depID = option.xpath("@value").extract()
            depID = str(depID[0])

            depUrl = "http://shopnsave.com/savings/view-ads/search-circular.html?category=%s&displayCount=500" % depID

            departments = option.xpath("text()").extract()
            print(departments)

            request = Request(url=depUrl)
            request.meta['department'] = departments
            yield request




