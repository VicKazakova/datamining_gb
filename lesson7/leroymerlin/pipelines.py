import hashlib

from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class LeroymerlinPipeline:
    def process_item(self, item, spider):
        return item


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [img[1] for img in results if img[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        photo_name = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f"{item['name']}/{photo_name}.jpg"
