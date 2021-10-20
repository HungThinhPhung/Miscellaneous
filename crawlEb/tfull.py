from load_example import example_url
import requests
from lxml import html
from to_html import to_html
import time
import pickle


def get_page(url):
    response = requests.get(url, timeout=10)
    html_page = html.fromstring(response.content.decode('utf-8'))
    output_title = html_page.cssselect("#chapter-big-container > div > div > h2 > a")[0].text_content().strip()
    output_content = ''
    text_content = html_page.get_element_by_id('chapter-c')
    paragraphs = text_content.findall('p')
    for p in paragraphs:
        output_content += '<p>{}</p>'.format(p.text_content().strip())
    if len(paragraphs) == 0:
        output_content += '<p>{}</p>'.format(text_content.text_content().strip())
    next_chapter_url = html_page.get_element_by_id('next_chap').attrib['href']
    return output_title, output_content, next_chapter_url


def get_total_data(base_url):
    next_url = base_url
    lst_title = []
    lst_content = []
    while not next_url == 'javascript:void(0)':
        output_title, output_content, next_url = get_page(next_url)
        lst_title.append(output_title)
        lst_content.append(output_content)
        time.sleep(1)
        print(next_url.split('-')[-1][:-1])
    return {'title': lst_title, 'content': lst_content}


if __name__ == '__main__':
    base_url = example_url['tfull']
    base_url = 'https://truyenfull.net/than-y-thanh-thu/chuong-1/'
    data = get_total_data(base_url)
    pickle.dump(data, open('data.p', 'wb'))
    to_html(data, 'TYTT')