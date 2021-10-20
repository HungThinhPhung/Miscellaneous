import os

import cv2
import numpy
import requests
import time
from img_processing import get_list_file


def download(url='https://www.tncnonline.com.vn/usercontrols/QTTJpegImage.aspx', extension='jpg', directory='img_file/', max_img=1000):
    if not directory.endswith('/'):
        directory += '/'
    for x in range(max_img):
        try:
            save_location = directory + str(int(time.time())) + '.' + extension
            content = requests.get(url, verify=False).content

            with open(save_location, 'wb') as f:
                f.write(content)

            time.sleep(1)
        except:
            time.sleep(1)
            continue


def check_all():
    dir = 'img_file/'
    files = get_list_file(dir)
    total = 0
    remove_lst = []
    for i in range(len(files) - 1):
        first_file = cv2.imread(dir + files[i])
        for j in range(i + 1, len(files)):
            second_file = cv2.imread(dir + files[j])
            if numpy.array_equal(first_file, second_file):
                total += 1
                print(files[i] + '\t' + files[j])
                remove_lst.append(files[j])
                break
    print(total)
    for f in remove_lst:
        os.remove(dir + f)


def check(file):
    dir = 'img_file/'
    files = get_list_file(dir)


if __name__ == '__main__':
    download(
        url='http://tracuunnt.gdt.gov.vn/tcnnt/captcha.png?uid=441c1083-94f2-4758-9688-a1104299d4b6',
        extension='png', directory='tracuu', max_img=510
    )
