import sys
import unittest
import os

from scrapy.http import Response
#We need to set the path two levels higher before importing the spider
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from storescraper.spiders.aldi_spider import AldiSpider


class AldiSpiderTest(unittest.TestCase):
    def setUp(self):
        self.aldiSpider = AldiSpider()



    def testParseLinks(self):

        response = self.setupResponse("aldi-main.html")

        departmentList = {"Beverages", "Cooler", "Dairy", "Fresh Bakery", "Fresh Produce",
                          "Frozen Foods", "Household", "New Low Price", "Pantry Items", "Plants & Flowers",
                          "Refrigerated Meats", "Seafood", "Snacks & Sweets"
                        }

        for request in self.aldiSpider.parseLinks(response):
            departmentList.remove(request.meta['department'])

        self.assertTrue(len(departmentList) == 0)


    def testParseItems(self):
        response = self.setupResponse("Beverages - Aldi Weekly Ad.html")

        items = self.aldiSpider.parseItems(response, "Beverages")
        self.assertEquals(10, len(items))

        item = items[0]

        self.assertEquals("Walker Napa Valley Red Wine", item['name'])
        self.assertEquals("9.99", item['price'])
        self.assertEquals("Beverages", item['department'])
        self.assertEquals("750 ml.", item['unit'])
        self.assertEquals("akimages.shoplocal.com/dyn_li/200.0.88.0/Retailers/Aldi/150114INS_HC2014_R_2884_Walker_NapaValleyRedWine_Hero.jpg",
                          item['imgLink'])



    def setupResponse(self, htmlPath):
        response = Response("test")
        response._set_body(open(os.path.dirname(__file__) + "/test_resources/" + htmlPath).read())
        return response
