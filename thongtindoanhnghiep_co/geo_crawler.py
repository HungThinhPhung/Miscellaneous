import json
import logging
import pickle

import requests

logging.basicConfig(filename='gov.log',level=logging.DEBUG)
def get_commune():
    i = 1

    communes = []
    while 1:
        try:
            response = requests.get('https://thongtindoanhnghiep.co/api/district/' + str(i) + '/ward')
            data = json.loads(response.content.decode("utf-8"))
            if len(data) == 0:
                break
            for d in data:
                communes.append(d['SolrID'])
            print(i)
        except:
            continue
        i += 1
    pickle.dump(communes, open('communes.p', 'wb'))
    return communes


def get_tax_code(start_idx=0):
    communes = pickle.load(open('communes.p', 'rb'))
    for commune in communes[start_idx:]:
        link = 'https://thongtindoanhnghiep.co/api/company?l=' + commune[1:] + '&p='
        p = 1
        while 1:
            try:
                response = requests.get(link + str(p))
                data = json.loads(response.content.decode("utf-8"))
                lst_items = data['LtsItems']
                if len(lst_items) == 0:
                    break
                for item in lst_items:
                    write_lines(item['MaSoThue'] + ': ' + item['Title'])
                logging.info(link + str(p))
            except:
                logging.error(link + str(p))
                continue
            p += 1


def write_lines(text: str):
    with open('data.txt', 'a') as f:
        f.write(text + '\n')
    f.close()


if __name__ == '__main__':
    get_tax_code()
