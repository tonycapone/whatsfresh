import sys
import unittest
import os
from scrapy.http import Request
from scrapy.http import Response
# We need to set the path two levels higher before importing the spider
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from storescraper.spiders.shopnsave_spider import ShopnsaveSpider


class ShopnSaveSpiderTest(unittest.TestCase):
    def setUp(self):
        self.shopnSaveSpider = ShopnsaveSpider()

    def testParseLinks(self):
        request = Request("http://test.com")
        response = self.setupResponse(request, "Shop 'n Save - Search Circular.html")

        departmentList = {"General Merchandise", "Grains, Pasta & Side Dishes", "Soups & Canned Goods",
                          "Specialty Food", "Floral", "Beer, Wine, Spirits & Tobacco", "Meat & Poultry",
                          "Fish & Seafood", "Frozen Foods", "Cooking & Baking", "Condiments", "Produce", "Snacks, Cakes & Desserts",
                           "Beverages", "Baby Food", "Dairy", "Deli", "Bakery", "Breakfast & Cereal"
        }

        for request in self.shopnSaveSpider.parseLinks(response):
            departmentList.remove(request.meta['department'])

        self.assertTrue(len(departmentList) == 0)

    def testParse(self):
        request = Request('http://test.com')
        request.meta["department"] = 'Grains, Pasta & Side Dishes'

        response = self.setupResponse(request, "Shop 'n Save - Grains and Pasta.html")
        items = self.shopnSaveSpider.parse(response)

        self.assertTrue(type(items) is list)
        self.assertEquals(5, len(items))

        item = items[0]

        self.assertEquals("Rice-A-Roni, Pasta-Roni or Cups", item['name'])
        self.assertEquals("10 for $10", item['price'])
        self.assertEquals("Grains, Pasta & Side Dishes", item['department'])
        self.assertEquals("akimages.shoplocal.com/dyn_li/185.0.75.0/Retailers/ShopnSave/150107_01_IL_V02_CIR_cmb_5.jpg",item['imgLink'])

    def testParseEmptyPage(self):
        request = Request('http://test.com')
        request.meta['depId'] = 11111
        request.meta['depIndex'] = 1
        request.meta["department"] = 'Produce'
        request.meta['items'] = []

        response = self.setupResponse(request, "Savealot - empty page.html")
        items = self.shopnSaveSpider.parse(response)
        self.assertTrue(type(items) is list)

        self.assertEquals(0, len(items))

    def setupResponse(self, request, htmlPath):
        response = Response(url='http://www.test.com',
        request=request,
        body=(open(os.path.dirname(__file__) + "/test_resources/" + htmlPath).read()))

        return response
