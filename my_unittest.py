import json
import os
import my_unittest
from os.path import isfile, join

import requests
import yaml

base_abs_path = '/home/phthinh/Projects/PycharmProjects/MISA.CVExtraction/resume/modules/testing/'
file_folder = base_abs_path + 'file/'
expect_folder = base_abs_path + 'expected_data/'
extract_folder = base_abs_path + 'extracted_data/'


def query(file_path):
    url = "http://localhost:8000/extract"
    headers = {}
    with open(file_path, 'rb') as f:
        body = f.read()
    response = requests.request("POST", url, headers=headers, data=body)
    text = response.text.replace('\\n', '|')
    data = list(json.loads(text)['data'].values())[0]
    data['personal']['avatar_image'] = True if data['personal']['avatar_image'] else False
    with open(extract_folder + '{}.yml'.format(os.path.basename(file_path).split('.')[0]), 'wt',
              encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, width=10000)
    return data


class TestSequense(my_unittest.TestCase):
    pass

    def assert_dict(self, act, exp):
        if type(act) != type(exp):
            self.fail('field is not match type: {} != {}'.format(type(act), type(exp)))
        if isinstance(act, str):
            self.assertEqual(act.strip(), exp.strip())
        elif isinstance(act, dict):
            for k in act:
                act_new = act[k]
                if k not in exp and not act[k]:
                    continue
                exp_new = exp[k]
                self.assert_dict(act_new, exp_new)
        elif isinstance(act, list):
            for i, item in enumerate(act):
                self.assert_dict(item, exp[i])
        elif isinstance(act, int):
            self.assertEqual(int(act), int(exp))
        elif act is None:
            self.assertTrue(exp is None)
        else:
            self.fail('unsupport type[{}]'.format(str(type(act))))

    def assert_result(self, json_obj, expected_file):
        with open(expected_file, 'rb') as f:
            expected_obj = yaml.safe_load(f)
        self.assert_dict(json_obj, expected_obj)


def test_generator(file_name):
    def test(self):
        result = query(file_folder + file_name)
        self.assert_result(result, expect_folder + file_name.split('.')[0] + '.yml')

    return test


def get_file_lst(directory):
    files = [f for f in os.listdir(directory) if isfile(join(directory, f))]
    return files


if __name__ == '__main__':
    arr = get_file_lst(file_folder)
    for t in arr:
        test_name = 'test_%s' % str(t)
        test = test_generator(t)
        setattr(TestSequense, test_name, test)

    my_unittest.main()
