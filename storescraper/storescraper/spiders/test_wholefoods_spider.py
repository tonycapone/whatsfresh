import sys
import unittest
import os
from scrapy.http import Request
from scrapy.http import Response
# We need to set the path two levels higher before importing the spider
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from storescraper.spiders.wholefoods_spider import WholeFoodsSpider


class TraderJoesSpiderTest(unittest.TestCase):
    def setUp(self):
        self.wholeFoodsSpider = WholeFoodsSpider()

    def testParse(self):
        request = Request('http://test.com')

        response = self.setupResponse(request, "Sales Flyer   Whole Foods Market.html")

        items = self.wholeFoodsSpider.parse(response)
        item = items[0]
        self.assertEquals(24, len(items))
        self.assertEquals("Hardbite Potato Chips", item['name'])
        self.assertEquals("$2.39", item['price'])
        self.assertEquals("ea", item['unit'])

    def setupResponse(self, request, htmlPath):
        response = Response(url='http://www.test.com',
        request=request,
        body=(open(os.path.dirname(__file__) + "/test_resources/" + htmlPath).read()))

        return response
