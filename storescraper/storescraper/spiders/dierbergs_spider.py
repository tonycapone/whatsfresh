# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.spider import Spider
from storescraper.items import StoreItem
from bs4 import BeautifulSoup
import re
import htmllib

import urlparse
class DierbergsSpider(Spider):
    name = "dierbergs"
    storestring = "Dierbergs"
    #allowed_domains = ["http://exposhopper.p2ionline.com"]
    start_urls = []
    imgBase = "http://exposhopper.p2ionline.com/Dierbergs/sitebase/"
    
    def start_requests(self):

        
        return [Request(url="http://exposhopper.p2ionline.com/Dierbergs/sitebase/index.aspx?area=search&adgroupid=227534",
        callback=self.parseLinks)]
    
    def parse(self, response):
            soup = BeautifulSoup(response.body)
            items = response.meta['items']

            for listing in soup.find_all("div", "bg_white"):
                item = StoreItem()
                item['name'] = listing.find("div", re.compile("headersub.?")).text
                caption = listing.find("div", re.compile("add_caption[0-9]"))
                if str(caption.contents[0]) != "<br/>":
                    item['unit'] = caption.contents[0]
                else:
                    item['unit'] = ""

                item['price'] = caption.strong.text
                item['department'] = response.meta["department"]

                item['store'] = 'Dierbergs'
                if (listing.find("img")["src"] != None):
                    item['imgLink'] = self.imgBase + listing.find("img")["src"]
                else:
                    item['imgLink'] = ""
                item['picData'] = ""
                items.append(item)
            if (soup.find("input", id="cntrlSearchResult_pgRptListItem_Page_Next") != None):
                request = FormRequest.from_response(
                    response,
                    formdata={
                        'cntrlSearchResult$pgRptListItem$Page$Next.x':'1',
                        'cntrlSearchResult$pgRptListItem$Page$Next.y':'1'
                    },
                    formname='frmHOM',
                    method='POST',
                    dont_click=True,
                    dont_filter=True,
                    callback=self.parse)
                request.meta['items'] = items
                request.meta["department"] = response.meta["department"]
                return request
            else:
                return items
    def parseLinks(self, response):
        soup = BeautifulSoup(response.body)

        categories = soup.find("select", {"name": "cntrlDeptList$DropDownList1"}).find_all("option")
        for category in categories[1:]:
            department = category.text
            depNum = category['value']
            depUrl = "http://exposhopper.p2ionline.com/Dierbergs/sitebase/index.aspx?area=search&adgroupid=227534&categoryid=%s" % depNum
            request = Request(url=depUrl)
            request.meta['department'] = department
            request.meta['items'] = []
            yield request

        