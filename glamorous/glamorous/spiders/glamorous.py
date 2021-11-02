from scrapy import Request
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import json

class Mixin:
    retailer = 'glamorous'
    allowed_domains = ['glamorous.com']
    start_urls = ['https://www.glamorous.com',]
    base_url = 'https://www.glamorous.com'

class GlomorousParseSpider(Mixin, Spider):
    name = Mixin.retailer + '-parse'

    def parse(self, response, **kwargs):

        data = response.css('script[id="ProductJson-product-template"]::text').get()
        if data:
            data_json = json.loads(data)

        
        product_id = data_json['id']
        title_desc = response.css('h2.name::text').get()
        price = response.css('span[itemprop="price"]::text').get()
        sizes = response.css('option::attr(value)').getall()
        availability = response.css('span[class="stock stock-product-template in-stock"]::text').get()
        if not title_desc:
            return
        sizes = [size for size in sizes if len(size)<=2]

        yield {
            "_values": {
                "retailer_sku": "",
                "gender": "",
                "category": [],
                "brand": "",
                "url": "",
                "retailer": "",
                "name": "",
                "description": [],
                "care": [],
                "image_urls": {
                    "colour": [
                        "https://"
                    ],
                    "colour": [
                        "https://"
                    ],
                    "colour": [
                        "https://"
                    ],
                    "colour": [
                        "https://"
                    ]
                    }
                }
            }

class GlomorousCrawlSpider(Mixin, CrawlSpider):
    name = Mixin.retailer + '-crawl'
    parse_spider = GlomorousParseSpider()

    listings_css = [
        '[id="megamenu-header-menu2"] ul',
        '[id=bc-sf-filter-bottom-pagination]',
    ]

    products_css = [
        'div[class="bc-sf-filter-product-item-inner"]',
    ]

    rules = [
        Rule(LinkExtractor(restrict_css=listings_css), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    ]

    # rules = [
    #     Rule(LinkExtractor(allow='collections/'), callback='parse_item', follow=True)
    # ]


    def parse(self, response, **kwargs):
        return super()._parse(response, **kwargs)

    def parse_item(self, response, **kwargs):
        return self.parse_spider.parse(response)



