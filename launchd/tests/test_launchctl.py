import os
import sys
import tempfile
import unittest
from typing import cast
from unittest.mock import patch

import launchd
from launchd import plist, service


def _make_fake_info(label, status=service.ServiceStatus.ENABLED, config=None):
    if config is None:
        config = {"Label": label, "OnDemand": True}
    plist_path = os.path.join(tempfile.gettempdir(), f"{label}.plist")
    return service.ServiceInfo(
        label=label,
        plist_path=plist_path,
        scope=plist.USER,
        status=status,
        config=config,
    )


class LaunchctlTestCase(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    @unittest.skipUnless(sys.platform.startswith("darwin"), "requires macOS")
    def test_examples(self):
        for job in launchd.jobs():
            self.assertTrue(type(job.pid) == int or job.pid == None)
            self.assertEqual(type(job.properties), dict)
            self.assertTrue("Label" in job.properties)
        # [job for job in launchd.jobs() if job.properties["Label"] is not None]

    @unittest.skipUnless(sys.platform.startswith("darwin"), "requires macOS")
    def test_jobs_generator(self):
        info = _make_fake_info("com.example.testjob")
        with patch(
            "launchd.launchctl.enumerate_services",
            return_value=iter([info]),
        ):
            jobs = list(launchd.jobs())
        self.assertEqual(1, len(jobs))
        job = jobs[0]
        self.assertIsInstance(job, launchd.LaunchdJob)
        self.assertEqual("com.example.testjob", job.label)
        props = cast(dict, job.properties)
        self.assertIsInstance(props, dict)
        self.assertTrue(props["Registered"])
        self.assertTrue(props["OnDemand"])
        self.assertEqual(info.plist_path, job.plistfilename)

    @unittest.skipUnless(sys.platform.startswith("darwin"), "requires macOS")
    def test_lazy_constructor_and_refresh(self):
        info = _make_fake_info("com.example.refresh")

        def _service_info(label):
            return info if label == info.label else None

        with patch("launchd.launchctl.get_service_info", side_effect=_service_info):
            job = launchd.LaunchdJob(info.label)
            self.assertTrue(job.exists())
            job.refresh()
            props = cast(dict, job.properties)
            self.assertIsInstance(props, dict)
            self.assertEqual(info.label, props["Label"])
            self.assertEqual(info.plist_path, job.plistfilename)
        with patch("launchd.launchctl.get_service_info", return_value=None):
            missing = launchd.LaunchdJob("com.example.missing")
            self.assertFalse(missing.exists())
            self.assertRaises(ValueError, missing.refresh)

    @unittest.skipUnless(sys.platform.startswith("darwin"), "requires macOS")
    def test_launchd_jobs_and_plist(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".plist") as fh:
            fh.write(b'<?xml version="1.0" encoding="UTF-8"?>')
            fh.flush()
            plist_path = fh.name
        try:
            info = service.ServiceInfo(
                label="com.example.temp",
                plist_path=plist_path,
                scope=plist.USER,
                status=service.ServiceStatus.ENABLED,
                config={"Label": "com.example.temp"},
            )
            with (
                patch(
                    "launchd.launchctl.enumerate_services",
                    return_value=iter([info]),
                ),
                patch(
                    "launchd.launchctl.get_service_info",
                    return_value=info,
                ),
            ):
                for job in launchd.jobs():
                    plist_path = job.plistfilename
                    self.assertIsNotNone(plist_path)
                    file_path = cast(str, plist_path)
                    self.assertTrue(os.path.isfile(file_path))
        finally:
            os.unlink(cast(str, plist_path))

    @unittest.skipUnless(sys.platform.startswith("darwin"), "requires macOS")
    def test_unsupported(self):
        label = "com.apple.Finder"
        job = launchd.LaunchdJob(label)
        self.assertRaises(AttributeError, lambda: print(job.laststatus))


    @unittest.skipUnless(sys.platform.startswith("darwin"), "requires macOS")
    def test_launchd_lazy_constructor(self):
        """This tests internal implementation."""
        # we assume that com.apple.Finder always exists and that it is always
        # running and always has a laststatus. Hmmmm.
        label = "com.apple.Finder"
        job = launchd.LaunchdJob(label)
        self.assertTrue(job.exists())
        self.assertFalse(hasattr(job, "_pid"))
        self.assertEqual({}, job._properties)
        job.refresh()
        self.assertNotEqual(None, job._pid)
        self.assertNotEqual(None, job.pid)
        self.assertNotEqual({}, job._properties)
