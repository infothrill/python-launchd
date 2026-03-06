Release history
---------------

1.0.0 (March 2026)
++++++++++++++++++
- Incompatible change: dropped support for `job.laststatus` (raises an exception)
- Bumped requirements of macOS (14+) as well as Python (3.10+)
- Adopted newer Apple SDK around SMAppService*
- Applied implicit Apple convention of lower-casing all unit ids
- Removed old python2 compatibility remnants (six, unicode)
- Modernized code style for python 3.10+
- Added __repr__ for launchd job ("LaunchdJob(label=com.apple.Finder)")

0.3.0 (June 2021)
+++++++++++++++++
- changed: create directory hierarchy for plist file if not present. issue #6
- improved: added automated flake8 tests, check-manifest and safety checks
- changed: moved basic CI to GitHub actions

0.2.0 (March 2021)
++++++++++++++++++
- drop python 2.x, 3.2, 3.3 support
- fix plistlib calls (issue #4)

0.1.2 (September 2020)
++++++++++++++++++++++
- added tox.ini for easier testing accross interpreter versions
- added travis test setup
- fixed incompatibility with `launchctl` in test code
- fixed a typo in the README

0.1.1 (November 2013)
+++++++++++++++++++++
- Fixed a bug in launchd.plist.read() when no scope was specified

0.1 (November 2013)
+++++++++++++++++++
- Focus: initial public release
