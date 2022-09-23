import numpy
import cv2
from PIL import Image


def calculate(image1, image2):
    image1 = cv2.cvtColor(numpy.asarray(image1), cv2.COLOR_RGB2BGR)
    image2 = cv2.cvtColor(numpy.asarray(image2), cv2.COLOR_RGB2BGR)
    hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
    hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
    # 计算直方图的重合度
    degree = 0
    for i in range(len(hist1)):
        if hist1[i] != hist2[i]:
            degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
        else:
            degree = degree + 1
    degree = degree / len(hist1)
    return degree


def classify_hist_with_split(image1, image2, size=(256, 256)):
    image1 = Image.open(image1)
    image2 = Image.open(image2)
    # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
    image1 = cv2.cvtColor(numpy.asarray(image1), cv2.COLOR_RGB2BGR)
    image2 = cv2.cvtColor(numpy.asarray(image2), cv2.COLOR_RGB2BGR)
    image1 = cv2.resize(image1, size)
    image2 = cv2.resize(image2, size)
    sub_image1 = cv2.split(image1)
    sub_image2 = cv2.split(image2)
    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)
    sub_data = sub_data / 3
    str_sub_data = int(str("%.2f%%" % (sub_data * 100)).split(".")[0])
    return str_sub_data


# if __name__ == '__main__':
#     img1_path = r"/Users/Fly/Desktop/vibe/app_check/screencap/at.cwiesner.android.visualtimer_202104079.apk.png"
#     img2_path = r"/Users/Fly/Desktop/vibe/app_check/screencap_bak/at.cwiesner.android.visualtimer_202104079.apk.png"
#     result = classify_hist_with_split(img1_path, img2_path)
#     print(result)