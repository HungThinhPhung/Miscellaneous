import datetime

import requests
import json
import time

base_ip = 'http://10.0.6.21'  # Dia chi ip den k8s
base_port = '30312'  # Dung lenh k get svc xem cua db
base_index = 'location_index_4'  # Index dang su dung, xem trong configmap
base_type = 'full_location_type'  # Type dang su dung, xem trong configmap
base_url = base_ip + ':' + base_port + '/' + base_index + '/' + base_type + '/'

old_id = 'VN22204'
old_loc_id = 'VN22519'
new_id = 'VN22193'
new_loc_id = 'VN22501'


# B1: Tim kiem huyen Hoanh Bo
def search_hb():
    pass


# B2: Tim kiem cac xa cua huyen Hoanh Bo và đổi id
def search_old_communes():
    query = {
        "query": {
            "bool": {
                "must": {
                    "term": {
                        "ParentID": old_loc_id.lower()
                    }
                }
            }
        }
    }
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    url = base_url + '_search'
    response = requests.post(url, json=query)
    result = json.loads(response.content.decode('utf-8'))
    result = result['hits']
    # if not result['total'] == 13:
    #     raise Exception
    hits = result['hits']
    output = {}
    for hit in hits:
        source = hit['_source']
        new_data = {
            "LocationID": source["LocationID"].replace(old_loc_id, new_loc_id),
            "ModifiedDate": now,
            "PostalCode": "",
            "ID": source["ID"].replace(old_id, new_id),
            "FullAddress": source["FullAddress"].replace("Huyện Hoành Bồ", "Thành phố Hạ Long"),
            "DistrictID": new_loc_id,
            "DID": new_id,
            "ParentID": new_loc_id
        }
        if source['ID'] == 'VN2220407030':
            new_data["LocationName"] = "Phường Hoành Bồ"
            new_data["FullAddress"] = new_data["FullAddress"].replace("Thị trấn Trới", "Phường Hoành Bồ")
            new_data["Suggestion"] = {
                "input": [
                    "Phường Hoành Bồ",
                    "Phuong Hoanh Bo",
                    "Hoành Bồ",
                    "Hoanh Bo"
                ]
            }
        output[hit['_id']] = new_data
    return output


# B3 Dem tong cac xa cua TP Ha Long
def count():
    query = {
        "query": {
            "bool": {
                "must": {
                    "term": {
                        "ParentID": new_loc_id.lower()
                    }
                }
            }
        }
    }
    url = base_url + '_count'
    response = requests.post(url, json=query)
    result = json.loads(response.content.decode('utf-8'))
    print(result["count"])


# B4 Doi Tat ca cac ID tuong ung: LocationID, ID, DistrictID, DID, ParentID, (PostalCode = '')
def change_id(input: dict):
    url = base_url + '{}/_update'
    for k, v in input.items():
        c_url = url.format(k)
        query = {
            "doc": v
        }
        response = requests.post(c_url, json=query)
        time.sleep(2)
        print(response.status_code)


# B5 Dem tong cac xa cua TP Ha Long sau khi chuyen
def check_count():
    pass


# B7 Xoa Huyen Hoanh Bo
def remove():
    query = {
        "query": {
            "bool": {
                "must": {
                    "term": {
                        "LocationID": old_loc_id.lower()
                    }
                }
            }
        }
    }
    url = base_url + '_search'
    response = requests.post(url, json=query)
    response = json.loads(response.content.decode('utf-8'))
    hits = response['hits']
    if not hits['total'] == 1:
        raise Exception
    id = hits['hits'][0]['_id']
    d_url = base_url + id
    d_response = requests.delete(d_url)
    print(d_response.status_code)
    print()


# count()
out = search_old_communes()
change_id(out)
count()
remove()
print()
