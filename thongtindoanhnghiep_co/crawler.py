import requests
import json
import pickle
from gov_crawler.gov_crawler.using_requests import get
from fuzzywuzzy import fuzz

def crawl_100k():
    import random
    base_link = 'https://thongtindoanhnghiep.co/api/company?r=100&p='
    ttdn_lst, gov_lst = [], []
    for i in range(1000):
        while not len(ttdn_lst) == i + 1:
            try:
                index = random.randint(1, 99)
                print('Page: ' + str(i + 1))
                response = requests.get(base_link + str(i + 1))
                data = json.loads(response.content.decode("utf-8"))
                tax_code = data['LtsItems'][index]['MaSoThue']
                ttdn_response = requests.get('https://thongtindoanhnghiep.co/api/company/' + str(tax_code))
                ttdn_data = json.loads(ttdn_response.content.decode("utf-8"))
                gov = get(tax_code, False)
                ttdn_lst.append(ttdn_data)
                gov_lst.append(gov)
            except:
                continue
    pickle.dump(ttdn_lst, open( "ttdn.p", "wb" ))
    pickle.dump(gov_lst, open( "gov.p", "wb" ))
    print()


def compare(d: dict, gov: dict):
    if len(gov) == 0:
        return False
    if fuzz.ratio(d['Title'].lower(), gov['ten_doanh_nghiep'].lower()) < 80:
        print(d['Title'].lower())
        print(gov['ten_doanh_nghiep'].lower())
        return False

    if fuzz.ratio(d['DiaChiCongTy'].lower(), gov['dia_chi_tru_so_chinh'].lower()) < 80:
        print(d['DiaChiCongTy'].lower())
        print(gov['dia_chi_tru_so_chinh'].lower())
        return False

    if not text2time(d['GiayPhepKinhDoanh_NgayCap']) == text2time(gov['ngay_thanh_lap']):
        print(text2time(d['GiayPhepKinhDoanh_NgayCap']))
        print(text2time(gov['ngay_thanh_lap']))
        return False

    return True


def text2time(text: str):

    result = []
    if '/' in text:
        result = text.split('/')
    if '-' in text:
        result = text[:10].split('-')
        result = result[::-1]
    return result


if __name__ == '__main__':
    ttdn = pickle.load(open('ttdn.p', 'rb'))
    gov = pickle.load(open('gov.p', 'rb'))
    total = 0
    count_none = 0
    error_list = []
    for i in range(1000):
        if compare(ttdn[i], gov[i]):
            total += 1
            continue
        if len(gov[i]) == 0:
            count_none += 1
            continue
        error_list.append(gov[i]['MST'])
    print(total)
    print(count_none)
    print(error_list)
    print()