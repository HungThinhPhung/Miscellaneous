from os import listdir
from os.path import isfile, join
from lxml import html

import requests
from lxml.html import HtmlElement


def get_taxcode_lst():
    directory = '/home/misa/PycharmProjects/test_only/gov_crawler/gov_crawler/data'
    files = [f.split('.')[0] for f in listdir(directory) if isfile(join(directory, f))]
    files.sort()
    return files


def send_request(taxcode: str):
    link = 'https://www.tncnonline.com.vn/Pages/TracuuMST.aspx'
    request_session = requests.session()
    home_page = request_session.get(link, verify=False)
    home_tree: HtmlElement = html.fromstring(home_page.content.decode('utf-8'))

    headers = {
        'Connection': "keep-alive",
        'Cache-Control': "max-age=0",
        'Origin': "https://www.tncnonline.com.vn",
        'Upgrade-Insecure-Requests': "1",
        'Content-Type': "application/x-www-form-urlencoded",
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'Referer': "https://www.tncnonline.com.vn/Pages/TracuuMST.aspx",
        'Accept-Encoding': "gzip, deflate, br",
        'Accept-Language': "en-US,en;q=0.9",
        'cache-control': "no-cache"
    }
    form_data = {
        '__SPSCEditMenu': 'true',
        'MSOWebPartPage_PostbackSource': '',
        'MSOTlPn_SelectedWpId': '',
        'MSOTlPn_View': 0,
        'MSOTlPn_ShowSettings': 'False',
        'MSOGallery_SelectedLibrary': '',
        'MSOGallery_FilterString': '',
        'MSOTlPn_Button': 'none',
        '__EVENTTARGET': 'ctl00$ctl12$g_e4936da3_53dd_4c77_b76a_b09e9bbed3f6$ctl42',
        '__EVENTARGUMENT': '',
        '__REQUESTDIGEST': home_tree.get_element_by_id('__REQUESTDIGEST').value,
        'MSOAuthoringConsole_FormContext': '',
        'MSOAC_EditDuringWorkflow': '',
        'MSOSPWebPartManager_DisplayModeName': 'Browse',
        'MSOWebPartPage_Shared': '',
        'MSOLayout_LayoutChanges': '',
        'MSOLayout_InDesignMode': '',
        'MSOSPWebPartManager_OldDisplayModeName': 'Browse',
        'MSOSPWebPartManager_StartWebPartEditingName': 'false',
        '__LASTFOCUS': '',
        '__VIEWSTATE': home_tree.get_element_by_id('__VIEWSTATE').value,
        '__VIEWSTATEGENERATOR': home_tree.get_element_by_id('__VIEWSTATEGENERATOR').value,
        '__EVENTVALIDATION': home_tree.get_element_by_id('__EVENTVALIDATION').value,
        'ctl00$ctl12$g_e4936da3_53dd_4c77_b76a_b09e9bbed3f6$LoaiTK': 'ctl42',
        'ctl00$ctl12$g_e4936da3_53dd_4c77_b76a_b09e9bbed3f6$txtCMT': '',
        'ctl00$ctl12$g_e4936da3_53dd_4c77_b76a_b09e9bbed3f6$txtSearchMST': '',
        'ctl00$ctl12$g_e4936da3_53dd_4c77_b76a_b09e9bbed3f6$ctl47': '',
    }
    bussiness_page = request_session.post(link, data=form_data, verify=False)
    bussiness_tree:HtmlElement = html.fromstring(bussiness_page.content.decode('utf-8'))

    captcha_img = request_session.get('https://www.tncnonline.com.vn/usercontrols/QTTJpegImage.aspx')
    with open('temp/tncn.aspx', 'wb') as f:
        f.write(captcha_img.content)
    form_data['__EVENTTARGET'] = ''
    form_data['__REQUESTDIGEST'] = bussiness_tree.get_element_by_id('__REQUESTDIGEST').value
    form_data['__VIEWSTATE'] = bussiness_tree.get_element_by_id('__VIEWSTATE').value
    form_data['__EVENTVALIDATION'] = bussiness_tree.get_element_by_id('__EVENTVALIDATION').value
    form_data['ctl00$ctl12$g_e4936da3_53dd_4c77_b76a_b09e9bbed3f6$ctl47'] = 'qwdqw'
    form_data['ctl00$ctl12$g_e4936da3_53dd_4c77_b76a_b09e9bbed3f6$txtSearchMST'] = taxcode,
    form_data['ctl00$ctl12$g_e4936da3_53dd_4c77_b76a_b09e9bbed3f6$ctl50'] = 'T%C3%ACm+ki%E1%BA%BFm'
    response = request_session.post(link, data=form_data, verify=False, headers=headers)
    print()


if __name__ == '__main__':
    tc = get_taxcode_lst()
    send_request(tc[0])
