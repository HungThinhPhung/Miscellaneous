import cv2
import pytesseract
from PIL import Image
import matplotlib.pylab as plt
import numpy as np
from math import sqrt, atan

from img_processing import get_list_file
import cv2


def tesseract_ocr2(link='/home/misa/PycharmProjects/test_only/img2txt/tracuu/train/42dhr.png'):
    src = cv2.imread(link, cv2.IMREAD_UNCHANGED)
    bgr = src[:, :, :3]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    alpha = src[:, :, 3]

    result = np.dstack([bgr, alpha])
    # image = plt.imread(link)
    cv2.imshow('image.jpg', alpha)
    cv2.waitKey(0)
    print()


def tesseract_ocr(link, show=False):
    # image = cv2.imread(link, cv2.IMREAD_UNCHANGED)
    image = plt.imread(link)
    image_2 = []
    [height, width, channel] = image.shape
    # 4 channel image to gray image
    for i in range(height):
        row = []
        image_2.append(row)
        for j in range(width):
            cell = 255 - int(image[i][j][3] * 255)
            cell = 255 if cell > 100 else 0
            row.append(cell)

    cr_img = crop_img(image_2, 30, 98, 0, 49)
    df_img = defish(cr_img, 0)
    img = np.array(df_img, dtype='uint8')
    plt.imshow(img, cmap=plt.cm.gray)
    plt.show()
    plt.imshow(image_2, cmap=plt.cm.gray)
    plt.show()
    print()
    # remove grid 1 line
    for k in range(2):
        for i in range(height):
            for j in range(width):
                if i in [0, height - 1] or j in [0, width - 1]:
                    image_2[i][j] = 255
                    continue
                if image_2[i][j] > 0:
                    continue
                if image_2[i - 1][j] > 0 and image_2[i + 1][j] > 0:
                    image_2[i][j] = 255
                    continue
                if image_2[i][j - 1] > 0 and image_2[i][j + 1] > 0:
                    image_2[i][j] = 255

    # remove grid 2 line
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if image_2[i][j] > 0:
                continue
            if image_2[i - 1][j] == 255 and image_2[i + 1][j] == 0 and image_2[i + 2][j] == 255:
                image_2[i][j] = 255
                image_2[i + 1][j] = 255
                continue
            if image_2[i][j - 1] == 255 and image_2[i][j + 1] == 0 and image_2[i][j + 2] == 255:
                image_2[i][j] = 255
                image_2[i][j + 1] = 255

    img = np.array(image_2, dtype='uint8')
    image_2 = cv2.cv2.blur(img, (3, 3))
    if show:
        plt.imshow(image_2, cmap=plt.cm.gray)
        plt.show()

    return pytesseract.image_to_string(image_2, config='-c tessedit_char_whitelist=23456789abcdefghkmnprwxy -oem 1')


def crop_img(arr_image: list, start_x, end_x, start_y, end_y):
    crop_img = []
    for i in range(start_y,end_y+1):
        row = []
        crop_img.append(row)
        for j in range(start_x, end_x + 1):
            row.append(arr_image[i][j])
    print((len(crop_img), len(crop_img[0])))
    return crop_img


def defish(arr_image, streng, room=1):
    max_x = len(arr_image[0])
    max_y = len(arr_image)
    half_x = max_x / 2
    half_y = max_y / 2
    result = []
    for i in range(max_y):
        row = []
        result.append(row)
        for j in range(max_x):
            row.append(arr_image[i][j])

    if streng == 0:
        streng = 0.000001
    correction_radius = sqrt(max_x * max_x + max_y * max_y) / streng
    for i in range(max_y):
        for j in range(max_x):
            new_x = j - half_x
            new_y = i - half_y
            distance = sqrt(new_x * new_x + new_y * new_y)
            r = distance / correction_radius
            if r == 0:
                theta = 1
            else:
                theta = atan(r) / r
            source_x = half_x + theta * new_x * room
            source_y = half_y + theta * new_y * room
            result[i][j] = arr_image[int(source_y)][int(source_x)]
    return result

if __name__ == '__main__':
    # train_dir = 'tracuu/train/'
    # files = get_list_file(train_dir)
    # count = 0
    # for file in files:
    #     link = train_dir + file
    #     t_ocr = tesseract_ocr(link).lower()
    #     if file[:-4] == t_ocr:
    #         count += 1
    #     # if file[:2] == t_ocr[:2] and file[5] == t_ocr[-1]:
    #     #     count += 1
    #     print(file[:-4] + '\t' + t_ocr)
    # print(count)

    print(tesseract_ocr('tracuu/train/42dhr.png', True))

    # tesseract_ocr2()
