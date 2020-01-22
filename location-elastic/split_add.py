import json

import requests

# from app import imap_search

e_host = 'http://0.0.0.0:9201/'
e_index = 'test_location/'
e_type = 'full_location_type/'
url = e_host + e_index + e_type
input_text = 'thắng lợi'

#
# def compare_local(selected_idx=0):
#     imap_search_data = imap_search(input_text)
#     selected_loc = imap_search_data[selected_idx]['properties']
#     first_loc = selected_loc['city'] if 'city' in selected_loc else selected_loc['name']
#     second_loc = selected_loc['state'] if 'state' in selected_loc else ''
#     final_loc = (first_loc + ' ' + second_loc).strip()
#     query = url + '_search?q=FullAddress:' + final_loc
#     response = json.loads(requests.get(query).content)
#     response_data = response['hits']['hits']
#     if len(response_data) == 0:
#         return []
#     for rd in response_data:
#         splitted_address = rd['_source']['FullAddress'].split(',')
#         if is_match_loc(first_loc, splitted_address) and is_match_loc(second_loc, splitted_address):
#             return splitted_address
#     return []


def resolve_loc(loc: str):
    if ',' not in loc and '-' not in loc:
        return []
    loc = loc.replace('-', ',')
    splitted_loc = [x.strip() for x in loc.split(',')]
    for i in range(len(splitted_loc)):
        query = url + '_search?q=LocationName:' + splitted_loc[i]
        response = json.loads(requests.get(query).content)
        hits = response['hits']['hits']
        for hit in hits:
            location_name = hit['_source']['LocationName']
            if not compare_add_string(location_name, splitted_loc[i]):
                continue
            full_address = hit['_source']['FullAddress']
            splitted_add = [x.strip() for x in full_address.split(',')]
            if compare_loc_add(splitted_loc, splitted_add, i):
                return splitted_add
    return []


def compare_loc_add(loc_lst: list, add_lst: list, start_point):
    for loc in loc_lst[start_point + 1:]:
        found = False
        for add in add_lst:
            if compare_add_string(add, loc):
                found = True
                break
        if not found:
            return False
    return True


def compare_add_string(add_1: str, add_2: str):
    return add_1.lower() in add_2.lower() or add_2.lower() in add_1.lower()


def is_match_loc(loc, splitted_address):
    for add in splitted_address:
        if loc in add or add in loc:
            return True
    return False


def add_lst_to_dict(add_lst: list) -> dict:
    result = {}
    add_lst.reverse()
    administration_name = ['country', 'province', 'district', 'commune']
    for i in range(4):
        result[administration_name[i]] = add_lst[i] if i < len(add_lst) else ''
    return result


if __name__ == '__main__':
    loc = 'huyện thường tín, hà nội'
    result = add_lst_to_dict(resolve_loc(loc))
    print(result)
