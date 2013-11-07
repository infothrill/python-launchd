# -*- coding: utf-8 -*-

import sys
import os
import unittest

from launchd import plist


class PlistToolTest(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_compute_filename(self):
        fname = plist.compute_filename("fubar", plist.USER)
        self.assertTrue('fubar.plist' in fname)
        self.assertTrue('/Library/LaunchAgents' in fname)
        self.assertFalse(fname.startswith('/Library/LaunchAgents'))

        fname = plist.compute_filename("fubar", plist.USER_ADMIN)
        self.assertTrue('fubar.plist' in fname)
        self.assertTrue(fname.startswith('/Library/LaunchAgents/'))

        fname = plist.compute_filename("fubar", plist.USER_OS)
        self.assertTrue('fubar.plist' in fname)
        self.assertTrue(fname.startswith('/System/Library/LaunchAgents/'))

        fname = plist.compute_filename("fubar", plist.DAEMON_ADMIN)
        self.assertTrue('fubar.plist' in fname)
        self.assertTrue(fname.startswith('/Library/LaunchDaemons/'))

        fname = plist.compute_filename("fubar", plist.DAEMON_OS)
        self.assertTrue('fubar.plist' in fname)
        self.assertTrue(fname.startswith('/System/Library/LaunchDaemons/'))

    @unittest.skipUnless(sys.platform.startswith("darwin"), "requires OS X")
    def test_discover_filename(self):
        fname = plist.discover_filename("com.apple.kextd", plist.DAEMON_OS)
        self.assertTrue(os.path.isfile(fname))

        # no scope specified
        fname2 = plist.discover_filename("com.apple.kextd")
        self.assertTrue(os.path.isfile(fname2))

        fname = plist.discover_filename("com.apple.kextd", plist.USER)
        self.assertEqual(None, fname)


class PlistToolPersistencyTest(unittest.TestCase):
    def setUp(self):
        self.sample_label = "com.example.unittest"
        self.sample_props = dict(Label="testlaunchdwrapper_python")
        fname = plist.discover_filename(self.sample_label, plist.USER)
        if fname is not None:
            os.unlink(fname)
        unittest.TestCase.setUp(self)

    def tearDown(self):
        fname = plist.discover_filename(self.sample_label, plist.USER)
        if fname is not None:
            os.unlink(fname)
        unittest.TestCase.tearDown(self)

    @unittest.skipUnless(sys.platform.startswith("darwin"), "requires OS X")
    def test_read_write(self):
        sample_label = "com.example.unittest"
        sample_props = dict(Label="testlaunchdwrapper_python")

        fname = plist.discover_filename(sample_label, plist.USER)
        self.assertEqual(None, fname)
        plist.write(sample_label, sample_props, plist.USER)

        fname = plist.discover_filename(sample_label, plist.USER)
        self.assertTrue(os.path.isfile(fname))
        props = plist.read(sample_label, plist.USER)
        self.assertEqual(sample_props, props)

        # read it without specifying the scope:
        props = plist.read(sample_label)
        self.assertEqual(sample_props, props)
