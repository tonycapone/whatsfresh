import sys
import unittest
import os
from mock import Mock
from scrapy.http import Request, TextResponse, FormRequest
from scrapy.http import Response
# We need to set the path two levels higher before importing the spider
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from storescraper.spiders.dierbergs_spider import DierbergsSpider


class DierbergsSpiderTest(unittest.TestCase):
    def setUp(self):
        self.dierbergsSpider = DierbergsSpider()

    def testParseLinks(self):
        request = Request('http://test.com')
        response = self.setupResponse(request, "dierbergs-main.html")

        departmentList = {"Bakery", "Beverages", "Canned Goods", "Cereal", "Cleaning Supplies", "Coffee/Tea/Cocoa",
                        "Condiments", "Cooking Supplies", "Dairy", "Deli", "Frozen Foods", "Grocery", "Health & Beauty",
                        "Ice Cream/Frozen Dessert", "Liquor", "Meat & Poultry", "Miscellaneous Grocery", "Paper Goods",
                        "Pasta/Sauce", "Pet Supplies", "Pharmacy", "Produce", "Seafood", "Snacks/Candy", "Uptown / Urban Furnishings"
                        }

        for request in self.dierbergsSpider.parseLinks(response):
            departmentList.remove(request.meta['department'])

        self.assertTrue(len(departmentList) == 0)

    def testParse1Page(self):
        request = Request('http://test.com')
        request.meta['department'] = 'Cleaning Supplies'
        request.meta['items']= []
        response = self.setupResponse(request, "dierbergs-cleaningsupplies.html")

        items = self.dierbergsSpider.parse(response)
        self.assertEquals(4, len(items))

        item = items[0]

        self.assertEquals("Airwick Freshmatic or Oil Refill", item['name'])
        self.assertEquals("$3.99", item['price'])
        self.assertEquals("Cleaning Supplies", item['department'])
        self.assertEquals("1-2 ct. pkg.", item['unit'])

    def testParse2Page(self):
        request = Request('http://test.com')
        request.meta['department'] = 'Bakery'
        request.meta['items']= []

        response = self.setupResponse(request, "dierbergs-bakery.html")

        request = self.dierbergsSpider.parse(response)
        self.assertTrue(type(request) is FormRequest)
        items = request.meta['items']
        item = items[0]

        self.assertEquals(u'Andrea\u2019s Cookies', item['name'])
        self.assertEquals("$6.49", item['price'])
        self.assertEquals("Bakery", item['department'])
        self.assertEquals("810 oz. pkg. Gluten Free", item['unit'])
    def setupResponse(self, request, htmlPath):

        response = TextResponse(url='http://www.test.com',
            request=request,
            body=(open(os.path.dirname(__file__) + "/test_resources/" + htmlPath).read()))

        return response