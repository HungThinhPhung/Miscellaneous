import scrapy


class GdMiiSpider(scrapy.Spider):
    name = 'gd_mii'

    def start_requests(self):
        start_urls = [
            'https://grimdawn.gamepedia.com/Monster_Infrequent_Items',
        ]
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        pass
