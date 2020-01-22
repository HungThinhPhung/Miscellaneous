import requests
from bs4 import BeautifulSoup


def get_all_link(table_content_id):
    soup = BeautifulSoup('data.html', "lxml")
    print(soup)


def crawl():
    pass


if __name__ == '__main__':
    p = 'http://help.misasme2017.misa.vn/'
    tc = 'div_javascript_contents'

    get_all_link(table_content_id=tc)
