def to_html(data, b_name, book_title=''):
    title = data['title']
    content = data['content']
    html_string = ''
    toc = ''
    for i in range(len(title)):
        html_string += '<h2 id=\"{}\">{}</h2><br>'.format(i, title[i])
        html_string += content[i]
        toc += '<a href=\"#{}\">{}</a></br>'.format(i, title[i])
    html_string = '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="vi" lang="vi"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><title>' + book_title + '</title></head><body><a name="toc" id="toc">' + toc + '<br><a name="start"></a><br><br>' + html_string + '</body>'
    with open(b_name + '.html', 'w') as f:
        f.write(html_string)
