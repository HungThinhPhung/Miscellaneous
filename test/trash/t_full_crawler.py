import pickle

import requests
from lxml import html
from lxml.cssselect import CSSSelector
from lxml.html import HtmlElement

url:str = pickle.load(open('example.p', 'rb'))
if not url.endswith('/'):
    url += '/'


def get_toc(url, last_toc=0):
    home_page = requests.get(url).content.decode('utf-8')
    home_page:HtmlElement = html.fromstring(home_page)
    lst_toc = home_page.cssselect('#list-chapter > ul')[0]
    if last_toc == 0:
        last_toc = get_last_toc(lst_toc)
    title = []
    content = []
    for i in range(1, last_toc+1):
        if i == 1:
            page = home_page
        else:
            base_url = url + 'trang-{}/#list-chapter'
            url = base_url.format(str(i))
            page = requests.get(url).content.decode('utf-8')
            page = html.fromstring(page)
        page_toc = page.cssselect('#list-chapter > div.row')[0]
        page_links = get_links(page_toc)
        for link in page_links:
            page_data = get_page_data(link)
            title.append(page_data['title'])
            content.append(page_data['content'])
        print()

    print()


def get_links(page_toc:HtmlElement):
    result = []
    for link in page_toc.iter('a'):
        result.append(link.attrib['href'])
    return result


def get_last_toc(lst_toc:HtmlElement):
    data = []
    for link in lst_toc.iter('a'):
        data.append(link.attrib['href'])
    last_page = data[-2]
    return int(''.join([x for x in last_page if x.isdigit()]))


def get_page_data(url):
    page = requests.get(url).content.decode('utf-8')
    page:HtmlElement = html.fromstring(page)
    title = str(page.cssselect('#wrap > div.container.chapter > div > div > h2 > a')[0].text_content())
    content = str(page.cssselect('#wrap > div.container.chapter > div > div > div.chapter-c')[0].text_content())
    return {'title': title, 'content': content}

def write_to_file(page_data:dict):
    pass


get_toc(url, 1)
