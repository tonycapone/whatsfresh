import sys
import unittest
import os
from mock import Mock
from scrapy.http import Request
from scrapy.http import Response
# We need to set the path two levels higher before importing the spider
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from storescraper.spiders.dierbergs_spider import DierbergsSpider


class DierbergsSpiderTest(unittest.TestCase):
    def setUp(self):
        self.dierbergsSpider = DierbergsSpider()

    def testParseLinks(self):
        response = self.setupResponse("dierbergs-main.html")

        departmentList = {"Bakery", "Beverages", "Canned Goods", "Cereal", "Cleaning Supplies", "Coffee/Tea/Cocoa",
                        "Condiments", "Cooking Supplies", "Dairy", "Deli", "Frozen Foods", "Grocery", "Health & Beauty",
                        "Ice Cream/Frozen Dessert", "Liquor", "Meat & Poultry", "Miscellaneous Grocery", "Paper Goods",
                        "Pasta/Sauce", "Pet Supplies", "Pharmacy", "Produce", "Seafood", "Snacks/Candy", "Uptown / Urban Furnishings"
                        }

        for request in self.dierbergsSpider.parseLinks(response):
            departmentList.remove(request.meta['department'])

        self.assertTrue(len(departmentList) == 0)

    def testParse1Page(self):
        response = self.setupResponse("dierbergs-cleaningsupplies.html")
        meta = {"department":'Cleaning Supplies',
                "items": []
        }
        response.meta = meta

        items = self.dierbergsSpider.parse(response )
        self.assertEquals(4, len(items))

        item = items[0]

        self.assertEquals("Airwick Freshmatic or Oil Refill", item['name'])
        self.assertEquals("$3.99", item['price'])
        self.assertEquals("Cleaning Supplies", item['department'])
        self.assertEquals("1-2 ct. pkg.", item['unit'])


    def setupResponse(self, htmlPath):
        response = Mock("Response")
        response.body = open(os.path.dirname(__file__) + "/test_resources/" + htmlPath).read()

        return response

