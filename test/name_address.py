import requests
import json
import logging
import traceback

def get_tax_codes(elastic_link, start_uid, size=1000):
    try:
        query_data = {"size": size, "query": {"match_all": {}},
                      "search_after": [start_uid],
                      "sort": [
                          {"_uid": "asc"}
                      ]}
        url = elastic_link + '_search'
        response = requests.post(url=url, json=query_data)
        response_data = json.loads(response.content.decode('utf-8'))
        return response_data['hits']['hits']
    except:
        logging.error(traceback.format_exc())
        return []

def execute(elastic_link, start_uid):
    tax_codes = get_tax_codes(elastic_link, start_uid)
    while not len(tax_codes) == 0:
        name_list = []
        add_list = []
        for code in tax_codes:
            source = code['_source']
            if len(source) == 0:
                continue
            name = source['owner']
            address = source['address']   
            name_list.append(name)
            add_list.append(address)
        
        with open('name.txt', 'a') as f:
            for n in name_list:
                n = smooth_data(n)
                if n == '':
                    continue
                f.writelines(n + '\n')
        
        with open('address.txt', 'a') as f:
            for n in add_list:
                n = smooth_data(n)
                if n == '':
                    continue
                f.writelines(n + '\n')
        last_code = tax_codes[-1]
        tax_codes = get_tax_codes(elastic_link, start_uid=last_code['_type'] + '#' + last_code['_id'])

def smooth_data(data:str):
    data = data.split('(')[0]
    return data.strip()

elastic_link = 'http://10.0.6.21:30152/sme_autocomplete_index/sme_autocomplete_type/'
execute(elastic_link, 0)