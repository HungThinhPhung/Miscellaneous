import textwrap

import requests
from lxml import html


def read(chapter):
    with open('/home/phthinh/Projects/PycharmProjects/test_only/test/reader/hidden.txt', 'r') as f:
        base_url = f.readline()
    url = base_url + str(chapter)
    page = requests.get(url, timeout=30)
    page_content = html.fromstring(page.content.decode('utf-8').replace('\r\n', '').strip())
    text_content = \
        page_content.cssselect('body > div.container.body-container > div > div.col-xs-12.chapter > div.chapter-c.max900 > div > div.box-chap')[0]
    data = str(text_content.text).replace('\t', '\n').strip()
    print(show_reconstructed_data(data, 150))


def show_reconstructed_data(data: str, max_length):
    data = data.split('\n')
    for d in data:
        new = textwrap.wrap(d, max_length, break_long_words=False)
        for line in new:
            print(line)


if __name__ == '__main__':
    read(235)
