from os import listdir
from os.path import isfile, join

dir = 'data'


def check_name():
    check_lst = 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789'
    saved_dict = {}
    for character in check_lst:
        saved_dict[character] = 0
    files = get_file_lst(dir)
    for file in files:
        for character in file:
            saved_dict[character] += 1
    result = [[], [], [], [], [], [], [], [], []]
    for k, v in saved_dict.items():
        result[v].append(k)
    for r in result:
        print(r)


def get_file_lst(directory):
    files = [f.split('.')[0] for f in listdir(directory) if isfile(join(directory, f))]
    files.sort()
    return files


if __name__ == '__main__':
    check_name()
