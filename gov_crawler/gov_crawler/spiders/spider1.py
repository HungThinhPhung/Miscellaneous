import time

import scrapy
from scrapy import cmdline
from scrapy.http import HtmlResponse
from scrapy_splash import SplashFormRequest, SplashRequest


class Spider1(scrapy.Spider):
    name = "spider1"

    def __init__(self, tax_code):
        self.tax_code = tax_code
        self.url = 'https://dangkyquamang.dkkd.gov.vn/inf/default.aspx'

    def start_requests(self):
        self.start_time = time.time()
        yield scrapy.Request(url=self.url, callback=self.search)

    def search(self, response:HtmlResponse):
        event_validation = response.css('#__EVENTVALIDATION').attrib['value']
        hd_param = response.css('#ctl00_hdParameter').attrib['value']
        form_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '',
            '__EVENTVALIDATION': event_validation,
            'ctl00$nonceKeyFld': '',
            'ctl00$hdParameter': hd_param,
            'ctl00$FldSearch': self.tax_code,
            'ctl00$FldSearchID': '',
            'ctl00$btnSearch': 'Tìm kiếm >>',
            'ctl00$searchtype': '1'
        }
        yield SplashFormRequest(url = self.url, formdata=form_data, callback=self.choose_result)

    def choose_result(self, response:HtmlResponse):
        result_table = response.css('#ctl00_C_UC_ENT_LIST1_CtlList')
        rows = result_table.css('tr')
        link_javascript = ''
        for row in rows:
            cells =  row.css('td')
            if not cells:
                continue
            if not cells[1].css('a::text').get() == self.tax_code:
                continue
            link_javascript = cells[0].css('a').attrib['href'][11:]
            break
        if not link_javascript:
            return {}
        yield SplashRequest(url=self.url, args={'js_source': link_javascript[11:]}, callback=self.parse)


    def parse(self, response):
        self.log('Xử lý 1 trong: ' + str(time.time() - self.start_time))

if __name__ == '__main__':
    tax_code = '0101243150'
    cmdline.execute(("scrapy crawl spider1 -a tax_code=" + tax_code).split())
