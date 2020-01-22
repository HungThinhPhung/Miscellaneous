import json
import pickle

import requests
from elastic.using_requests import get_gov

demo_tax_codes = pickle.load(open('error.p', 'rb'))

host = 'http://0.0.0.0:9201'
host = 'http://10.0.6.21:30152'
e_index = 'index'
e_index = 'sme_autocomplete_index_2'
e_type = 'sme_autocomplete_type'
default_link = host + '/' + e_index + '/' + e_type + '/'


def get(tax_code):
    link = 'http://10.0.6.21:30152/sme_autocomplete_index/sme_autocomplete_type/_search?q=taxCode:' + tax_code + '&size=1'
    response = requests.get(link)
    response = json.loads(response.content.decode('utf-8'))

    return response['hits']['hits'][0] if not len(response['hits']['hits']) == 0 else {}


def add_doc(data):
    json_sent = data['_source']
    link = 'http://0.0.0.0:9201/' + data['_index'] + '/' + data['_type'] + '/' + json_sent['taxCode']

    response = requests.put(link, json=json_sent)
    print()


def get_tax_codes(start_uid=0, size=10):
    query_data = {"size": size, "_source": ["taxCode", "tax_code"], "query": {"match_all": {}},
                  "search_after": [start_uid],
                  "sort": [
                      {"_uid": "asc"}
                  ]}
    url = default_link + '_search'
    response = requests.post(url=url, json=query_data)
    response_data = json.loads(response.content.decode('utf-8'))
    return response_data['hits']['hits']


def update(id, d):
    link = default_link + id + '/_update'
    script = {
        "script": "ctx._source.remove('eng_name'); "
                  "ctx._source.remove('short_name');"
                  "ctx._source.remove('tax_code');"
                  "ctx._source.remove('name');"
                  "ctx._source.remove('active_status');"
                  "ctx._source.remove('enterprise_type');"
                  "ctx._source.remove('founding_date');"
                  "ctx._source.remove('legal_representative');"
                  "ctx._source.owner='" + d['legal_representative'] + "';"
                                                                      "ctx._source.address='" + d['address'] + "';"
                                                                                                               "ctx._source.engName='" + d[
                      'eng_name'] + "';"
                                    "ctx._source.shortName='" + d['short_name'] + "';"
                                                                                  "ctx._source.taxCode='" + d['tax_code'] + "';"
                                                                                                                            "ctx._source.companyName='" +
                  d['name'] + "';"
                              "ctx._source.activeStatus='" + d['active_status'] + "';"
                                                                                  "ctx._source.enterpriceType='" + d['enterprise_type'] + "';"
                                                                                                                                          "ctx._source.foundedDate='" +
                  d['founding_date'] + "';"
                                       "ctx._source.verify=1;"
    }
    response = requests.post(link, json=script)
    if not response.status_code == 200:
        print()


def main():
    tax_codes = get_tax_codes()
    while not len(tax_codes) == 0:
        for code in tax_codes:
            if len(code['_source']) == 0:
                tax_code = code['_id']
            else:
                tax_code = code['_source']['taxCode'] if 'taxCode' in code['_source'] else code['_source']['tax_code']
            print('Id: ' + code['_id'] + ', taxCode: ' + tax_code)
            data = get_gov(tax_code, False)
            if len(data) == 0:
                print('Error')
                continue
            update(code['_id'], data)
        last_code = tax_codes[-1]
        tax_codes = get_tax_codes(start_uid=last_code['_type'] + '#' + last_code['_id'])


if __name__ == '__main__':
    # for code in demo_tax_codes:
    #     data = get(code)
    #     if data == {}:
    #         continue
    #     add_doc(data)
    main()
