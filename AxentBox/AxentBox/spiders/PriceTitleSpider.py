from os import name
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Mixin:
    retailer = 'fashiondays'
    allowed_domains = ['fashiondays.bg']
    start_urls = ['https://www.fashiondays.bg', ]
    base_url = 'https://www.fashiondays.bg'

class FashionParseSpider(Mixin, Spider):
    name = Mixin.retailer + '-parse'

    def parse(self, response, **kwargs):
        title = response.css('h1.product-brand-desc::text').get()
        price_lv = response.css('span.new-price > span::text').get()
        price_st = response.css('span.new-price > span > i::text').get()
        price = price_lv + '.' + price_st
        title = title[2:].strip()[1:-2]

        yield {
            'title': title,
            'price': price,
        }

class FashionCrawlSpider(Mixin, CrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = FashionParseSpider()

    rules = [Rule(LinkExtractor(allow='p/'), callback='parse_item', follow=True)]

    def parse_item(self, response):
        return self.parse_spider.parse(response)

