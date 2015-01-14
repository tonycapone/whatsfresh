import sys
import unittest
import os
from scrapy.http import Request
from scrapy.http import Response
# We need to set the path two levels higher before importing the spider
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from storescraper.spiders.savealot_spider import SaveALotSpider


class SaveALotSpiderTest(unittest.TestCase):
    def setUp(self):
        self.saveAlotSpider = SaveALotSpider()

    def testParseLinks(self):
        request = Request("http://test.com")
        response = self.setupResponse(request, "SaveALot Weekly Ad - St. Louis.html")

        departmentList = {"Bulk", "Dairy and Frozen", "General Merchandise",
                          "Meat and Seafood", "Produce",  "Shockingly Low Prices"
        }

        for request in self.saveAlotSpider.parseLinks(response):
            departmentList.remove(request.meta['department'])

        self.assertTrue(len(departmentList) == 0)

    def testParseMultiplePages(self):
        request = Request('http://test.com')
        request.meta['depId'] = 11111
        request.meta['depIndex'] = 1
        request.meta["department"] = 'Produce'
        request.meta['items'] = []

        response = self.setupResponse(request, "Produce - SaveALot Weekly Ad.html")
        request = self.saveAlotSpider.parse(response)
        self.assertTrue(type(request) is Request)
        items = request.meta['items']

        self.assertEquals(8, len(items))

        item = items[0]

        self.assertEquals("Dole Classic Iceberg Salad Mix", item['name'])
        self.assertEquals(u'99 ea', item['price'])
        self.assertEquals("Produce", item['department'])
        self.assertEquals("akimages.shoplocal.com/dyn_li/120.0.88.0/Retailers/SaveALot/150111wk3_262_p4_p1_9a.jpg",item['imgLink'])

    def testParseEmptyPage(self):
        request = Request('http://test.com')
        request.meta['depId'] = 11111
        request.meta['depIndex'] = 1
        request.meta["department"] = 'Produce'
        request.meta['items'] = []

        response = self.setupResponse(request, "Savealot - empty page.html")
        items = self.saveAlotSpider.parse(response)
        self.assertTrue(type(items) is list)

        self.assertEquals(0, len(items))

    def setupResponse(self, request, htmlPath):
        response = Response(url='http://www.test.com',
        request=request,
        body=(open(os.path.dirname(__file__) + "/test_resources/" + htmlPath).read()))

        return response
