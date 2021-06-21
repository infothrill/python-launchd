Release history
---------------

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
