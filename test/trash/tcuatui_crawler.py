import requests
from lxml import html
from lxml.cssselect import CSSSelector
from lxml.html import HtmlElement
from hyper.contrib import HTTP20Adapter

def get_toc(url:str, start_chapter=0):
    name = url.split('/')[-1]
    sess =  requests.sessions.Session()
    sess.mount('https://truyencuatui.net', HTTP20Adapter())
    home_page = sess.get(url).content.decode('utf-8')
    
    # Create header
    header = {
        ':authority': 'truyencuatui.net',
        ':method': 'GET',
        ':path': '/chuong/' + name,
        ':scheme': 'https'
    }
    response = sess.get('https://truyencuatui.net' + '/chuong/' + name)
    print()

test_url = 'https://truyencuatui.net/truyen/kanagawa-sinh-vien-dao-si.html'
get_toc(test_url)