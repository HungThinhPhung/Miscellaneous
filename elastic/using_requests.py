import json
import time
from os import listdir
from os.path import isfile, join

import requests
from lxml import html, cssselect
from lxml.html.clean import clean_html
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_gov(tax_code, write_to_file=True):
    try:
        start_time = time.time()

        # Gọi trang chủ để khởi tạo session và lấy tham số
        home_url = 'https://dangkyquamang.dkkd.gov.vn/inf/default.aspx'
        request_session = requests.sessions.Session()
        home_page = request_session.get(home_url, verify=False)
        home_tree = html.fromstring(home_page.content)
        event_validation = home_tree.get_element_by_id('__EVENTVALIDATION').value
        hd_param = home_tree.get_element_by_id('ctl00_hdParameter').value

        # Gọi trang Search lấy secret ID của doanh nghiệp
        search_url = 'https://dangkyquamang.dkkd.gov.vn/inf/Public/Srv.aspx/GetSearch'
        search_form = {
            "searchField": tax_code,
            "h": hd_param
        }
        try_times = 0
        while try_times < 20:
            try:
                search_headers = {'content-type': 'application/json', 'charset': 'UTF-8'}
                search_response = request_session.post(search_url, json=search_form, headers=search_headers)
                search_data = json.loads(search_response.text)['d']
                break
            except:
                time.sleep(1)
                try_times += 1
                continue
        secret_id = ''
        for org in search_data:
            if org['Enterprise_Gdt_Code'] == tax_code:
                secret_id = org['Id']

        # Gọi trang kết quả tìm kiếm, trích rút thông tin
        form_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': '',
            '__EVENTVALIDATION': event_validation,
            'ctl00$nonceKeyFld': '',
            'ctl00$hdParameter': hd_param,
            'ctl00$FldSearch': tax_code,
            'ctl00$FldSearchID': secret_id,
            'ctl00$btnSearch': 'Tìm kiếm >>',
            'ctl00$searchtype': 1
        }
        result_page = request_session.post(home_url, data=form_data, verify=False)
        result_tree = html.fromstring(clean_html(result_page.text.replace('</br>', '<br>').replace('\r', '').replace('\n', '').replace('\t', '')))

        #
        # for br in result_tree.cssselect("br"):
        #     br.tail = "\n" + br.tail if br.tail else "\n"

        name = normalize(result_tree.get_element_by_id('ctl00_C_NAMEFld', ''))
        if name == '':
            return {}
        eng_name = normalize(result_tree.get_element_by_id('ctl00_C_NAME_FFld', ''))
        short_name = normalize(result_tree.get_element_by_id('ctl00_C_SHORT_NAMEFld', ''))
        active_status = normalize(result_tree.get_element_by_id('ctl00_C_STATUSNAMEFld', ''))
        active_status = 1 if active_status == 'Đang hoạt động' else 0
        enterprise_type = normalize(result_tree.get_element_by_id('ctl00_C_ENTERPRISE_TYPEFld', ''))
        founding_date = normalize(result_tree.get_element_by_id('ctl00_C_FOUNDING_DATE', ''))
        founding_date = change_date_type(founding_date)
        legal_representative = normalize(result_tree.cssselect('#ctl00_C_Tab1 > div:nth-child(8) > p:nth-child(1) > span.viewInput.viewSearch'))
        address = normalize(result_tree.get_element_by_id('ctl00_C_HO_ADDRESS', ''))
        i_table = result_tree.get_element_by_id('i_Data', {})
        if write_to_file:
            with open('data/' + tax_code + '.yaml', 'w') as f:
                f.write('tax_code: "' + tax_code + '"\n')
                f.write('name: "' + name + '"\n')
                f.write('eng_name: "' + eng_name + '"\n')
                f.write('short_name: "' + short_name + '"\n')
                f.write('active_status: "' + str(active_status) + '"\n')
                f.write('enterprise_type: "' + enterprise_type + '"\n')
                f.write('founding_date: "' + founding_date + '"\n')
                f.write('legal_representative: "' + legal_representative + '"\n')
                f.write('address: "' + address + '"\n')
                f.write('time: "' + str(time.time() - start_time) + '"')
            f.close()
        request_session.close()
        return {
            'tax_code': tax_code,
            'name': name,
            'eng_name': eng_name,
            'short_name': short_name,
            'active_status': str(active_status),
            'enterprise_type': enterprise_type,
            'founding_date': founding_date,
            'legal_representative': legal_representative,
            'address': address
        }
    except Exception as e:
        return {}


def normalize(data):
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        return data[0].text.strip() if len(data) > 0 else ''
    return data.text.strip() if data.text is not None else ''


def change_date_type(date: str):
    if date is None or date == '':
        return ''
    date_lst = date.split('/')
    return date_lst[2] + '-' + date_lst[1] + '-' + date_lst[0]


if __name__ == '__main__':
    data = get_gov('0101243151', False)
    print()

    # directory = '/home/misa/Desktop/CrawlerORGINFO/thongtincongty.co/storage/decription'
    # files = [f for f in listdir(directory) if isfile(join(directory, f))]
    # files.sort()
    # error_list = []
    # for file in files:
    #     try:
    #         get(file[:-4])
    #         print(file)
    #     except Exception as e:
    #         error_list.append(file[:-4])
    #         print('Sai: ' + file)
    #         print(e)
    #         continue
    # error_list2 = []
    # for e in error_list:
    #     try:
    #         get(e)
    #     except:
    #         error_list2.append(e)
    # print(error_list2)
