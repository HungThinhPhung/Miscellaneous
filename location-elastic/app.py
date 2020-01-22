import json

import requests
from flask import Flask, request, render_template
from split_add import add_lst_to_dict, resolve_loc

import tone_marks

host = 'http://0.0.0.0:9201/'
index = 'test_location'
app = Flask(__name__)


def suggest_query(text: str):
    url = host + index + '/_suggest'
    json_send = {
        "location": {
            "text": text,
            "completion": {
                "field": "Suggestion",
                "size": 10
            }
        }
    }
    response = requests.post(url, json=json_send)
    if response.status_code not in [200, 201]:
        print('Response status code: ' + response.status_code)
        return None
    return response


def process(input_text):
    input_text = input_text.strip()
    response = suggest_query(input_text)
    data = json.loads(response.content)
    suggest_lst = data['location'][0]['options']

    if len(suggest_lst) == 0:
        input_text = tone_marks.remove_tm_string(input_text)
    response = suggest_query(input_text)
    data = json.loads(response.content)
    suggest_lst = data['location'][0]['options']
    for s in suggest_lst:
        print(s['_source']['FullAddress'])
    return suggest_lst


def loop_process(text):
    result = process(text)
    unused = ''
    while len(result) == 0 and not text.strip() == '':
        text_lst = text.split(' ')
        unused += ' ' + text_lst[0]
        text_lst = text_lst[1:]
        text = ' '.join(text_lst).strip()
        result = process(text)

    for res in result:
        res['_source']['FullTyping'] = unused.title() + ', ' + res['_source']['FullAddress']
    return result


@app.route('/', methods=["GET"])
def render_index():
    return render_template("index.html")


@app.route('/myapi', methods=["GET"])
def main():
    input_text = request.args.get('text')
    response = []
    splitted_text = input_text.replace('-', ',').split(',')
    for text in splitted_text:
        response += loop_process(text)
    return json.dumps(response)


@app.route('/imap', methods=["GET"])
def imap():
    input_text = request.args.get('text')
    return json.dumps(imap_search(input_text))


def imap_search(input_text):
    response = requests.get(url='https://map.itrithuc.vn/geocode2/api/',
                            params={'q': input_text, 'lat': '16.1024476', 'lon': '106.0078059', 'location_bias_scale': '2'})
    data = json.loads(response.content.decode('utf-8'))

    return data['features']


#
@app.route('/split', methods=["GET"])
def split():
    input_text = request.args.get('text')
    result = add_lst_to_dict(resolve_loc(input_text))
    return json.dumps(result, ensure_ascii=False).encode('utf8')



if __name__ == '__main__':
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["JSON_SORT_KEYS"] = False
    app.config["JSON_AS_ASCII"] = False
    # regis_consul()
    app.run(debug=True, port=10000, host="0.0.0.0", threaded=True)
