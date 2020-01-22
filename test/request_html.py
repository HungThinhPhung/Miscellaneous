def send(pages):
    import requests
    import time
    while True:
        for page in pages:
            try:
                requests.get(page)
                time.sleep(25)
            except:
                continue


if __name__ == '__main__':
    page_list = ['https://social.msdn.microsoft.com/Search/en-us/vscom?query=set+up&pgArea=header&Refinement=198&ac=2#refinementChanges=&pageNumber=2&showMore=false',
                 'https://social.msdn.microsoft.com/Search/en-us/vscom?query=install&pgArea=header&Refinement=198&ac=4',
                 'https://visualstudio.microsoft.com/vs/support/',
                 'https://support.google.com/search?q=install&from_promoted_search=true',
                 'https://support.google.com/search?q=setup'
                 ]
    send(page_list)