from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class Mixin:
    retailer = 'glamorous'
    allowed_domains = ['glamorous.com']
    start_urls = ['https://www.glamorous.com',]
    base_url = 'https://www.glamorous.com'

class GlomorousParseSpider(Mixin, Spider):
    name = Mixin.retailer + '-parse'
    def parse(self, response, **kwargs):
        title_desc = response.css('h2.name::text').get()
        price = response.css('span[itemprop="price"]::text').get()
        sizes = response.css('option::attr(value)').getall()
        availability = response.css('span[class="stock stock-product-template in-stock"]::text').get()
        if not title_desc:
            return
        sizes = [size for size in sizes if len(size)<=2]
        yield {
            'title_desc': title_desc,
            'price': price,
            'sizes': sizes,
            'availability': availability
        }


class GlomorousCrawlSpider(Mixin, CrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = GlomorousParseSpider()

    rules = [Rule(LinkExtractor(allow='collections/'), callback='parse_item', follow=True)]

    def parse_item(self, response, **kwargs):
        return self.parse_spider.parse(response)



