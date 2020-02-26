from scrapy import Spider, Request
from scrapy.http import Response


class NoJSSpider(Spider):
    name = 'no_js'

    def start_requests(self):
        start_urls = [
            'http://0.0.0.0:8111/',
        ]
        for url in start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response:Response):
        h1_text = response.css('h1')[0].root.text
        print(h1_text)



