# -*- coding: utf-8 -*-

import unittest
import sys
import os

import launchd

launchdtestplist = dict(
          Disabled=False,
          Label="testlaunchdwrapper_python",
          Nice=-15,
          OnDemand=True,
          ProgramArguments=["/bin/bash", "-c", "echo 'Hello World' && exit 0"],
          RunAtLoad=True,
          ServiceDescription="runs a sample command",
          ServiceIPC=False,
          )


class LaunchctlTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    @unittest.skipUnless(sys.platform.startswith("darwin"), "requires OS X")
    def test_examples(self):
        activejobs = [job for job in launchd.jobs() if job.pid is not None]
        inactivejobs = [job for job in launchd.jobs() if job.pid is None]
        errorjobs = [job for job in launchd.jobs() if job.laststatus != 0 and job.laststatus is not None]
        ondemandjobs = [job for job in launchd.jobs() if job.properties['OnDemand'] is True]

    @unittest.skipUnless(sys.platform.startswith("darwin"), "requires OS X")
    def test_launchctl_jobs(self):
        jobs = launchd.jobs()
        self.assertFalse(isinstance(jobs, list))  # it's a generator!
        for job in jobs:
            self.assertTrue(isinstance(job, launchd.LaunchdJob))
            self.assertTrue(isinstance(job.properties, dict))
            if job.pid is not None:
                # this fails sometimes due to short lived processes that
                # have disappeared by the time we reach this test
                self.assertEqual(job.pid, job.properties['PID'], "pid equality")
            else:
                self.assertTrue('PID' not in job.properties)

    @unittest.skipUnless(sys.platform.startswith("darwin"), "requires OS X")
    def test_launchctl_jobs_and_plist(self):
        for job in launchd.jobs():
            if job.plistfilename is not None:
                self.assertTrue(os.path.isfile(job.plistfilename))
