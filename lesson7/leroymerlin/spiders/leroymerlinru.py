import scrapy
from scrapy.http import HtmlResponse
from leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.start_urls = [f'https://leroymerlin.ru/catalogue/kaktusy-i-sukkulenty/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@data-qa-pagination-item, 'right')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@data-qa, 'product-name')]")
        for link in links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photos', "//img[@alt='product image']/@src")
        yield loader.load_item()
