import requests
import json
from lxml import html
import time
import pickle


def get_data(b_name, chapter):
    base_link = 'https://truyenyy.com/truyen/{}/chuong-{}.html'.format(b_name, chapter)
    response = requests.get(base_link, timeout=15)
    res_data = html.fromstring(response.content)
    body = res_data.body
    title = body.cssselect('div > div > h1')[0].text_content().strip()
    content = body.cssselect('div > div > div > div')[2].text_content()
    return title, content


def to_html(data, b_name):
    title = data['title']
    content = data['content']
    print(len(title))
    print(len(content))
    html_string = ''
    toc = ''
    for i in range(len(title)):
        html_string += '<h2 id=\"{}\">{}</h2><br>'.format(i, title[i])
        html_string += '<p>' + content[i] + '</p>'
        toc += '<a href=\"#{}\">{}</a></br>'.format(i, title[i])
    html_string = '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="vi" lang="vi"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><title>Nhà đầu tư thông minh - Sai</title></head><body><a name="toc" id="toc">' + toc + '<br><a name="start"></a><br><br>' + html_string + '</body>'
    with open(b_name + '.html', 'w') as f:
        f.write(html_string)


if __name__ == '__main__':
    b_name = 'ngan-ho'
    # data = {}
    # title_lst = []
    # content_lst = []
    # try:
    #     for i in range(1, 948):
    #         print(i)
    #         title, content = get_data(b_name, i)
    #         title_lst.append(title)
    #         content_lst.append(content)
    #         time.sleep(1)
    # except:
    #     print()
    # data['title'] = title_lst
    # data['content'] = content_lst
    # pickle.dump(data, open('ngan-ho.p', 'wb'))
    # print()

    data = pickle.load(open('ngan-ho.p', 'rb'))
    to_html(data, b_name)