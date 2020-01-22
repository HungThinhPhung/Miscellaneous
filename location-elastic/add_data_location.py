import json
import tone_marks
import requests
from elasticsearch import Elasticsearch

elastic_host = '0.0.0.0'
# elastic_host = '10.0.6.21'
elastic_port = '9201'
# elastic_port = '30152'
elastic_index = 'test_location'
elastic_document_type = 'full_location_type'
# elastic_type_countries = cfg.elastic_type_countries
# elastic_type_provinces = cfg.elastic_type_provinces
# elastic_type_districts = cfg.elastic_type_districts
# elastic_type_wards = cfg.elastic_type_wards


es = Elasticsearch([{'host': elastic_host, 'port': elastic_port}])
with open('FullLocation.json') as json_file:
    data = json.load(json_file)
    print(data)


def add_2():
    prefix_administration = ['Huyện', 'Xã', 'Phường', 'Thị trấn', 'Tỉnh', 'Quận', 'Huyện', 'Nước', 'Quốc gia', 'Thành phố']
    cnt = 1
    for location in data:
        if 'Quận 1' in location['LocationName']:
            print(location)
        location['UsedCount'] = 0
        suggest_data = [location['LocationName']]
        rm_tm = tone_marks.remove_tm_string(location['LocationName'])
        rm_pre = None
        rm_pre_tm = None
        for pre in prefix_administration:
            if location['LocationName'].startswith(pre):
                rm_pre = location['LocationName'].replace(pre, '').strip()
                rm_pre_tm = tone_marks.remove_tm_string(rm_pre)
                break
        for d in [rm_tm, rm_pre, rm_pre_tm]:
            if d is not None and any(c.isalpha() for c in d) and d not in suggest_data:
                suggest_data.append(d)

        location['FullAddress'] = get_full_address(location)
        location['Suggestion'] = {"input": suggest_data}
        # response = requests.post('http://' + elastic_host + ':' + elastic_port + '/' + elastic_index + '/' + elastic_document_type, json=location)
        # if response.status_code not in [200, 201]:
        #     raise Exception(response.status_code)

        print("Inserted: " + str(cnt))
        cnt += 1


def add():
    with open('FullLocation.json') as json_file:
        data = json.load(json_file)
        print(data)
        count = 0
        cnt = 1
        for location in data:
            location['UsedCount'] = 0
            es.index(index=elastic_index, doc_type=elastic_document_type, body=location)
            print("Inserted: " + str(cnt))
            cnt += 1


def find_parent(loc):
    if loc['Kind'] == 0 or 'VN' not in loc['LocationID']:
        return None
    parent_id = loc['ParentID']
    for d in data:
        if d['LocationID'] == parent_id:
            return d
    return None


def get_full_address(loc):
    result = loc['LocationName']
    loc_2 = find_parent(loc)
    while loc_2 is not None:
        result += ', ' + loc_2['LocationName']
        loc_2 = find_parent(loc_2)
    return result


def search_company_by_company_name(input_field):
    """
    :param input_field:  the input what user typed
    :return: item list that matched to the query
    """
    input_field = input_field.rstrip(" ")
    elastic_search_data = {
        "query": {
            "match_phrase": {
                "companyName": {
                    "query": input_field
                }
            }
        }
    }
    result = es.search(index=elastic_index, body=elastic_search_data)
    result_list = list()

    for item in result['hits']['hits']:
        if len(result_list) > 10:
            break
        result_list.append({"taxCode": item['_source']['taxCode'], "companyName": item['_source']['companyName']})
    return result_list


if __name__ == '__main__':
    add_2()
