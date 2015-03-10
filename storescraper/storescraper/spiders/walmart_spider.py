# coding=utf-8
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector

from ..items import StoreItem
from bs4 import BeautifulSoup
import urlparse
import re

class WalmartSpider(Spider):
    storestring = "Walmart"
    name = "walmart"
    start_urls = []

    def start_requests(self):

        return [Request(url="http://weeklyads.walmart.com/flyers/walmartusa-circular/grid_view/44609?chrome=broadsheet&locale=en-US&type=2",
        callback=self.parseLinks)]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "html5lib")
        items = []

        for itemListing in soup.find("div", class_="items-list").ul.find_all("li", class_="item"):
            item = StoreItem()
            item['name']= itemListing.find("div", class_="item-name").get_text()
            priceLine = itemListing.find("div", class_="item-price").get_text()
            priceLine = priceLine.replace('\n', '')
            item['price'] = priceLine[:(priceLine.find(".")+3)].strip()
            unit = priceLine[priceLine.find(u'¢')+1:]
            item['unit'] = unit.strip()
            item['imgLink'] = itemListing.find("div", class_="img-wrapper").find("img")['src']
            item['department'] = response.meta['department']
            item['store'] = "Walmart"
            item['picData'] = ""

            items.append(item)
        return items


    def parseLinks(self, response):
        urlBase = "http://weeklyads.walmart.com/"
        soup = BeautifulSoup(response.body, "html5lib")


        for departmentLink in soup.find("div", class_="real-category-list").find_all("a")[1:]:
            department = departmentLink.get_text().split('\n')[0]
            url = urlBase + departmentLink['href']

            request = Request(url)
            request.meta['department'] = department
            yield request


