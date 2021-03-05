# -*- coding: utf-8 -*-

import unittest

import six

from launchd import cmd


class LaunchdCmdTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testlaunchctl_invalid_args(self):
        self.assertRaises(ValueError, cmd.launchctl, ['foo'])

    def testlaunchctl_list(self):
        stdout = cmd.launchctl("list").decode("utf-8")
        self.assertTrue(isinstance(stdout, six.string_types))

    def testlaunchctl_list_x(self):
        label = "com.apple.Finder"
        stdout = cmd.launchctl("list", label).decode("utf-8")
        self.assertTrue(isinstance(stdout, six.string_types))
