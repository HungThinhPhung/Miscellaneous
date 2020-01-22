from os import listdir
from os.path import isfile, join
import cow.patterns.singleton

train1 = '/home/misa/PycharmProjects/test_only/img2txt/tracuu/train'
val1 = '/home/misa/PycharmProjects/test_only/img2txt/tracuu/val'
train2 = '/home/misa/NetBeansProjects/CaptchaGen/data/train'
val2 = '/home/misa/NetBeansProjects/CaptchaGen/data/val'
test2 = '/home/misa/NetBeansProjects/CaptchaGen/data/test'

pools = [
    '2345678abcdefghkmnprwxy'
]


def get_list_file(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    print('Length: ' + str(len(files)))
    return files


def character_pool(files):
    result = ''
    for file in files:
        for character in file:
            if character not in result:
                result += character
    return ''.join(sorted(result))


def main():
    v1 = get_list_file(test2)
    print(character_pool(v1))


t1 = get_list_file(train2)
t2 = get_list_file(val2)
t3 = get_list_file(test2)


def create_dataset():
    for file in t1[:10]:
        name = file.split('.')[0]
        with open('crnn-data/' + name + '.txt', 'w') as f:
            f.write(name)
        with open('crnn-data/train', 'a') as f:
            f.write(file + '\n')

def copy_f():
    import shutil
    source_train = '/home/misa/NetBeansProjects/CaptchaGen/data/train/'
    source_test = '/home/misa/NetBeansProjects/CaptchaGen/data/val/'
    target = '/home/misa/NetBeansProjects/CaptchaGen/data/data'
    i = 0
    for file in t1:
        i += 1
        if i % 1000 == 0:
            print(i)
        shutil.copy(source_train + file, target)
    i = 0
    for file in t2:
        i += 1
        if i % 1000 == 0:
            print(i)
        shutil.copy(source_test + file, target)

