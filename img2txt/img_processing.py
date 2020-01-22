from os import listdir
from os.path import isfile, join
import matplotlib.pylab as plt
from PIL import Image
import numpy as np
import pytesseract
import cv2


def get_list_file(directory):
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    files.sort()
    return files


def get_distance(x, y):
    return (x[0] - y[0]) * (x[0] - y[0]) + (x[1] - y[1]) * (x[1] - y[1]) + (x[2] - y[2]) * (x[2] - y[2])


dir = 'img_file/'
files = get_list_file(dir)


def process_plt():
    # for i in range(1, 30):
    #     np_img = cv2.imread(dir + files[i])
    #
    #     # for i in range(3):
    #     #     pli_img = plt.imread(dir + files[i+7])
    #     #     plt.imshow(pli_img)
    #     #     plt.show()
    #
    #     np_copy = np_img.copy()
    #     (row_num, col_num, rgb) = np_copy.shape
    #
    #     gray_img = []
    #     for i in range(row_num):
    #         r = []
    #         gray_img.append(r)
    #         for j in range(col_num):
    #             v = int(sum(np_copy[i][j])/3)
    #             r.append(v if v > 20 and v < 170 else 255)
    #     plt.imshow(gray_img, 'gray')
    #     plt.show()
    # print()

    np_img = cv2.imread(dir + files[-1])
    np_copy = cv2.resize(np_img, None, fx=3, fy=3)
    (row_num, col_num, rgb) = np_copy.shape
    for i in range(row_num):
        for j in range(col_num):
            pixel = np_copy[i][j]
            # if pixel[2] <= 195 and pixel[1] >= 190 and pixel[0] >= 190:
            if pixel[2] < min(pixel[1], pixel[0]):
                np_copy[i][j] = [0, 0, 0]

    plt.imshow(np_copy)
    plt.show()
    bl_img = cv2.blur(np_copy, (3, 3))
    gau_bl_img = cv2.GaussianBlur(np_img, (3, 3), 0)

    medi_bl_img = cv2.medianBlur(np_copy, 3)
    # medi_bl_img = cv2.medianBlur(medi_bl_img, 3)
    cv2.imshow('image', medi_bl_img)
    cv2.waitKey(0)

    # plt.imshow(gau_bl_img)
    # plt.show()
    print(pytesseract.image_to_string(medi_bl_img))
    print()


def get_text(img):
    text = pytesseract.image_to_string(img)
    print(text)


def process_cv2():
    img = cv2.imread(dir + files[-1])

    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = to_bin_img(img, 60, 150)
    img = fill_img(img)
    # img = cv2.medianBlur(img, 3)
    img = cv2.resize(img, None, fx=5, fy=5)
    print(get_text(img))
    cv2.imshow('image', img)
    cv2.waitKey(30000)


def to_bin_img(img, threshold_1, threshold_2=None):
    (row_num, col_num) = img.shape
    for i in range(row_num):
        for j in range(col_num):
            if threshold_2 is None:
                img[i][j] = 0 if img[i][j] < threshold_1 else 255
            else:
                img[i][j] = 0 if img[i][j] > threshold_1 and img[i][j] < threshold_2 else 255
    return img


def fill_img(img):
    result_img = None
    while not np.array_equal(result_img, img):
        result_img = img.copy()
        (row_num, col_num) = img.shape
        for i in range(1, row_num - 1):
            for j in range(1, col_num - 1):
                count = 0

                for m in range(3):
                    for n in range(3):
                        if m == 1 and n == 1:
                            continue
                        if img[i - 1 + m][j - 1 + n] == 0:
                            count += 1
                if count >= 6:
                    img[i][j] = 0
    return result_img


if __name__ == '__main__':
    process_cv2()
