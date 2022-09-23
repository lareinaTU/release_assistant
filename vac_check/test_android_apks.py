import os
import unittest
from parameterized import parameterized

from image_similarity import classify_hist_with_split


def get_images_data():
    path = '/Users/Fly/Desktop/vibe/app_check/screencap/'
    bak_path = '/Users/Fly/Desktop/vibe/app_check/screencap_bak/'

    files = os.listdir(path)
    image_data = []

    for file in files:
        image_data.append([path + file, bak_path + file])
    return image_data


class AddTestCase(unittest.TestCase):

    @parameterized.expand(get_images_data())
    def test_add(self, img_expect, img_actual):
        self.assertGreater(classify_hist_with_split(img_expect, img_actual), 90)

