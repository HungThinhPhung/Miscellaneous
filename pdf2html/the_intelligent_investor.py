import pickle

# from pdf2html.reader import PdfReader
#
# file_loc = '/home/phthinh/temp/pack/IntInvestor.pdf'
# file = open(file_loc, 'rb')
# pdf_reader = PdfReader(file)
# data = pdf_reader.get_data()
# pickle.dump(data, open('the_intelligent_investor.p', 'wb'))

data = pickle.load(open('the_intelligent_investor.p', 'rb'))
pages_number = []
html_string = ''


def check_title(text: str):
    text_spl = text.split(' ')
    for t in text_spl:
        if t.islower():
            return False
    return True


i = 1
for page in data:
    pages_number.append(i)
    html_string += '<h2 id=\"{page_num}\">{page_num}</h2><p>'.format(page_num=i)
    i += 1
    for line in page:
        if line.strip().isdigit():
            continue
        if line == '\n':
            html_string += '</p><p>'
        else:
            html_string += ' ' + line.replace('. \n', '.</br>') if not check_title(line) else line.replace('\n', '</br>')
    if not html_string.endswith('</p>'):
        html_string += '</p>'

toc = ''
for pn in pages_number:
    toc += '<a href=\"#{pgn}\">{pgn}</a></br>'.format(pgn=pn)
html_string = '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="vi" lang="vi"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /><title>Nhà đầu tư thông minh - Sai</title></head><body><a name="toc" id="toc">' + toc + '<br><a name="start"></a><br><br>' + html_string + '</body>'
with open('the_intelligent_investor.html', 'w') as f:
    f.write(html_string)
