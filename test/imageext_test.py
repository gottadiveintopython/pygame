# -*- coding: utf8 -*-
import os
import os.path
import sys
import unittest

from pygame.tests.test_utils import example_path
import pygame, pygame.image, pygame.pkgdata
from pygame.compat import as_unicode, unicode_
imageext = sys.modules['pygame.imageext']

class ImageextModuleTest( unittest.TestCase ):
    # Most of the testing is done indirectly through image_test.py
    # This just confirms file path encoding and error handling.
    def test_save_non_string_file(self):
        im = pygame.Surface((10, 10), 0, 32)
        self.assertRaises(TypeError, imageext.save_extended, im, [])

    def test_load_non_string_file(self):
        self.assertRaises(pygame.error, imageext.load_extended, [])

    def test_save_bad_filename(self):
        im = pygame.Surface((10, 10), 0, 32)
        u = as_unicode(r"a\x00b\x00c.png")
        self.assertRaises(pygame.error, imageext.save_extended, im, u)

    def test_load_bad_filename(self):
        u = as_unicode(r"a\x00b\x00c.png")
        self.assertRaises(pygame.error, imageext.load_extended, u)

    def test_save_unknown_extension(self):
        im = pygame.Surface((10, 10), 0, 32)
        s = "foo.bar"
        self.assertRaises(pygame.error, imageext.save_extended, im, s)

    def test_load_unknown_extension(self):
        s = "foo.bar"
        self.assertRaises(pygame.error, imageext.load_extended, s)

    def test_load_unicode_path(self):
        u = unicode_(example_path("data/alien1.png"))
        im = imageext.load_extended(u)

    def test_save_unicode_path(self):
        temp_file = u"你好.png".encode('utf8')
        im = pygame.Surface((10, 10), 0, 32)
        try:
            os.remove(temp_file)
        except EnvironmentError:
            pass
        self.assert_(not os.path.exists(temp_file))
        try:
            imageext.save_extended(im, temp_file)
            self.assert_(os.path.getsize(temp_file) > 10)
        finally:
            try:
                os.remove(temp_file)
            except EnvironmentError:
                pass

if __name__ == '__main__':
    unittest.main()
