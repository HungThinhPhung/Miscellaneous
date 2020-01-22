import re
from os import listdir
from os.path import isfile, join
import yaml


def get_file_lst(directory):
    files = [f.split('.')[0] for f in listdir(directory) if isfile(join(directory, f))]
    files.sort()
    return files


files1 = get_file_lst('/home/misa/Desktop/CrawlerORGINFO/thongtincongty.co/storage/decription/')
files2 = get_file_lst('/home/misa/PycharmProjects/test_only/gov_crawler/gov_crawler/data/')


def check_length():
    print(len(files1))
    print(len(files2))


def check_empty():
    times = []
    for name in files2:

        with open('/home/misa/PycharmProjects/test_only/gov_crawler/gov_crawler/data/' + name + '.yaml', 'rb') as file:
            data = yaml.load(file)
            times.append(data['thoi_gian_xu_ly'])
            if not data['ten_doanh_nghiep']:
                print(name)
                continue
    print(len(times))
    print(sum([float(x) for x in times]) / len(times))


def recontruc_line(line):
    l = line.split(':')
    if len(l) == 1:
        return l[0] + ': ""\n'
    else:
        return l[0] + ': "' + l[1].strip() + '"\n'


def clean():
    for name in files2:
        with open('/home/misa/PycharmProjects/test_only/gov_crawler/gov_crawler/data/' + name + '.yaml', 'r') as f:
            file_lines = [x for x in f.readlines() if re.search('[a-zA-Z]+', x)]

        with open('/home/misa/PycharmProjects/test_only/gov_crawler/gov_crawler/data/' + name + '.yaml', 'w') as f:
            f.writelines(file_lines)


if __name__ == '__main__':
    check_empty()
