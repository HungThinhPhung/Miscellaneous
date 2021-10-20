import scrapy
from scrapy.http import Response
from scrapy_splash import SplashRequest


class JSSpider(scrapy.Spider):
    name = 'js'

    def start_requests(self):
        start_urls = [
            'http://759292f4.ngrok.io/',
        ]

        for url in start_urls:
            yield SplashRequest(url, callback=self.parse)

    def parse(self, response:Response):
        h1_text = response.css('h1')[0].root.text
        print(h1_text)
