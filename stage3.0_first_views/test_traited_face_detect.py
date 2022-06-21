from os.path import dirname, join
from unittest import TestCase

import numpy as np

import ets_tutorial
from traited_face_detect import ImageFile

TUTORIAL_DIR = dirname(ets_tutorial.__file__)

SAMPLE_IMG_DIR = join(TUTORIAL_DIR, "..", "sample_images")

SAMPLE_IMG1 = join(SAMPLE_IMG_DIR, "IMG-0311_xmas_2020.JPG")


class TestImageFile(TestCase):
    def test_no_image_file(self):
        img = ImageFile()
        self.assertEqual(img.metadata, {})
        data = img.to_array()
        self.assertIsInstance(data, np.ndarray)
        self.assertEqual(data.shape, (0,))

    def test_image_metadata(self):
        img = ImageFile(filepath=SAMPLE_IMG1)
        self.assertNotEqual(img.metadata, {})
        for key in ['ExifVersion', 'ExifImageWidth', 'ExifImageHeight']:
            self.assertIn(key, img.metadata.keys())
        data = img.to_array()
        expected_shape = (img.metadata['ExifImageHeight'],
                          img.metadata['ExifImageWidth'], 3)
        self.assertEqual(data.shape, expected_shape)

    def test_detects_faces(self):
        img = ImageFile(filepath=SAMPLE_IMG1)
        self.assertEqual(len(img.faces), 5)
        self.assertEqual(img.metadata["Number of faces"], 5)
