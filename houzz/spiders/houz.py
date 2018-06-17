# -*- coding: utf-8 -*-
import scrapy, json, urllib
from scrapy.utils.response import open_in_browser
from houzz.items import HouzzItem

BaseURL = "https://www.houzz.com.au"
GoogleURL = "https://script.google.com/macros/s/AKfycbya3T7dcbunoow22WfI0jtyJYvUIYa8fW0vgs8A3vP0YOFfUqvu/exec"
Counter = 0

class HouzSpider(scrapy.Spider):
    name = 'houzz'
    allowed_domains = ['www.houzz.com']
    start_urls = [ BaseURL + "/professionals/c/Australia"]

    def parse(self, response):
        global Counter
        for Category in response.xpath("//form[@id='leftFilters']//a[@class='sidebar-item-label']"):
            #Counter += 1
            #if Counter == 1:
            CategoryTitle = Category.xpath("normalize-space(./span/text())")[0].extract()
            CategoryHref = Category.xpath("normalize-space(./@href)")[0].extract()
            MetaData = {
                "Category Title"    :   CategoryTitle,
                "Category Href"     :   CategoryHref
            }
            if "http" in CategoryHref:
                yield scrapy.Request(CategoryHref, callback=self.parse_categories, dont_filter=True, meta=MetaData)
                #break
    
    def parse_categories(self, response):
        for Post in response.xpath("//div[contains(@class,'browseListBody ')]/div[contains(@class,'whiteCard ')]"):
            PostTitle = Post.xpath(".//div[@class='name-info']/a/text()")[0].extract()
            PostHref = Post.xpath(".//div[@class='name-info']/a/@href")[0].extract()
            MetaData = {
                "category"  :   response.meta['Category Title'],
                "posttitle" :   urllib.quote(PostTitle.encode('utf-8')),
                "posthref"  :   PostHref,
            }
            if "http" in PostHref:
                yield scrapy.Request(PostHref, meta=MetaData, callback=self.parse_details, dont_filter=True)
        try:
            NextPageLink = response.xpath("//li/a[@class='navigation-button next']/@href")[0].extract()
            if "http" in NextPageLink:
                yield scrapy.Request(NextPageLink, callback=self.parse_categories, dont_filter=True, meta=response.meta)
        except:
            pass

    def parse_details(self, response):
        items = HouzzItem()
        # make sure only un-cached / new records are saved in the spreadsheet
        if not "cached" in response.flags:
            try:
                PhoneNumber = response.xpath("//div[@compid='Profile_Phone']/span[@class='pro-contact-text']/text()")[0].extract()
            except:
                PhoneNumber = "-"
            try:
                ContactPersonRAW = response.xpath("normalize-space(//div[@class='info-list-text']/b[text()='Contact']/../text())")[0].extract()
                ContactPerson = ContactPersonRAW.split(": ")[1]
            except:
                ContactPerson = "-"
            try:
                LocationRAW = response.xpath("//div[@class='info-list-text']/b[text()='Location']/..")
                try:
                    Street = LocationRAW.xpath("./span[@itemprop='streetAddress']/text()")[0].extract()
                except:
                    Street = "-"
                try:
                    AddressLocality = LocationRAW.xpath("./span[@itemprop='addressLocality']/text()")[0].extract()
                except:
                    AddressLocality = "-"
                try:
                    AddressRegion = LocationRAW.xpath("./span[@itemprop='addressRegion']/text()")[0].extract()
                except:
                    AddressRegion = "-"
                try:
                    PostalCode = LocationRAW.xpath("./span[@itemprop='postalCode']/text()")[0].extract()
                except:
                    PostalCode = "-"
                try:
                    AddressCountry = LocationRAW.xpath("./span[@itemprop='addressCountry']/text()")[0].extract()
                except:
                    AddressCountry = "-"
                Location = Street + ", " + AddressLocality + ", " + AddressRegion + ", " + PostalCode + ", " + AddressCountry
            except:
                Location = "-"
            items["category"] = response.meta['category'],
            items["posttitle"] = response.meta['posttitle'],
            items["posthref"] = response.meta['posthref'],
            items["location"] = Location,
            items["contact"] = ContactPerson,
            items["phone"] = PhoneNumber
            yield items
            print "Item processed!"
            #yield scrapy.FormRequest(GoogleURL, formdata=DataObject, callback=self.dummy, method="POST", dont_filter=True, meta={"refresh_cache":True})
        else:
            pass
    
    def dummy(self, response):
        pass
