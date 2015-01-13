import sys
import unittest
import os
from scrapy.http import Request
from scrapy.http import Response
# We need to set the path two levels higher before importing the spider
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from storescraper.spiders.traderjoes_spider import TraderJoesSpider


class TraderJoesSpiderTest(unittest.TestCase):
    def setUp(self):
        self.traderJoesSpider = TraderJoesSpider()

    def testParseLinks(self):
        request = Request("http://test.com")
        response = self.setupResponse(request, "Fearless Flyer   Trader Joe's.html")

        departmentList = {"Bakery", "Beverages", "Cheese", "Grocery", "Frozen", "Produce & Flowers",
                          "Refrigerated Products", "Snacks & Sweets", "Supplements & Such", "Wine & Beer"
                         }

        for request in self.traderJoesSpider.parseLinks(response):
            departmentList.remove(request.meta['department'])

        self.assertTrue(len(departmentList) == 0)

    def testParse(self):
        request = Request('http://test.com')
        request.meta["department"] = 'Beverages'

        response = self.setupResponse(request, "Spiced Chai Trader Joe's.html")
        item = self.traderJoesSpider.parse(response)

        self.assertEquals("Spiced Chai", item['name'])
        self.assertEquals("$1.99", item['price'])
        self.assertEquals("Beverages", item['department'])
        self.assertEquals("www.traderjoes.com/images/fearless-flyer/uploads/article-2081/52053-spiced-chai.jpg",item['imgLink'])

    def testParseCategory(self):
        request = Request("http://test.com")
        request.meta['department'] = "Beverages"
        response = self.setupResponse(request, "Beverages Category Trader Joe's.html")

        links = {"http://www.traderjoes.com/fearless-flyer/article/2081",
                 "http://www.traderjoes.com/fearless-flyer/article/2101"}
        for request in self.traderJoesSpider.parseCategory(response):
            links.remove(request.url)



    def setupResponse(self, request, htmlPath):
        response = Response(url='http://www.test.com',
        request=request,
        body=(open(os.path.dirname(__file__) + "/test_resources/" + htmlPath).read()))

        return response

