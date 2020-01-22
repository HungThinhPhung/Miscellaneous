import random
from os import listdir, rename
from os.path import isfile, join

url = '/home/misa/NetBeansProjects/CaptchaGen/data/'


def get_file_lst(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    return files


def random_list(lst:list):
    random.shuffle(lst)
    return lst

def split(lst_file):
    lst_train = lst_file[:650000]
    lst_val = lst_file[650000:790000]
    lst_test = lst_file[790000:]

    # Move train
    for file in lst_train:
        old = url + file
        new = url + 'train/' + file
        rename(old, new)

    for file in lst_val:
        old = url + file
        new = url + 'val/' + file
        rename(old, new)

    for file in lst_test:
        old = url + file
        new = url + 'test/' + file
        rename(old, new)

def main():
    files = get_file_lst(url)
    files = random_list(files)
    split(files)


def run1():
    train = get_file_lst(url + 'train')
    val = get_file_lst(url + 'val')
    test = get_file_lst(url + 'test')

    t1 = [x for x in train if x in val]
    t2 = [x for x in train if x in test]
    t3 = [x for x in val if x in test]

    print(t1)
    print(t2)
    print(t3)
