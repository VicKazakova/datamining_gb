import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def clear_price(value):
    try:
        value = int(value.replace('\xa0', ''))
    except:
        pass
    return value


class LeroymerlinItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(default=None, output_processor=TakeFirst(), input_processor=MapCompose(clear_price))
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
