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
