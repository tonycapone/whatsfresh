# coding=utf-8
import sys
import unittest
import os
from mock import Mock
from scrapy.http import Request
from scrapy.http import Response
# We need to set the path two levels higher before importing the spider
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from storescraper.spiders.walmart_spider import WalmartSpider


class WalmartSpiderTest(unittest.TestCase):
    def setUp(self):
        self.walmartSpider = WalmartSpider()

    def testParseLinks(self):
        response = self.setupResponse(Request("http://test.com"), "Walmart.html")

        departmentList = {"Clothing, Shoes & Jewelry", "Electronics & Office",
        "Grocery, Household & Pets", "Pharmacy, Health & Beauty", "Rollback", "Other"
        }

        for request in self.walmartSpider.parseLinks(response):
            departmentList.remove(request.meta['department'])

        self.assertTrue(len(departmentList) == 0)

    def testParse(self):
        request = Request("http://walmart.com")
        request.meta['department'] = "Grocery"

        response = self.setupResponse(request, "Walmart.html")


        items = self.walmartSpider.parse(response)
        item = items[0]
        self.assertEquals(202, len(items))
        self.assertEquals(u'7UP® Ten® 2 Liter', item['name'])
        self.assertEquals("$1.00" , item['price'])
        self.assertEquals("each", item['unit'])
        self.assertEquals("Grocery", item['department'])


    def setupResponse(self, request, htmlPath):
        response = Response(url='http://www.test.com',
        request=request,
        body=(open(os.path.dirname(__file__) + "/test_resources/" + htmlPath).read()))

        return response
