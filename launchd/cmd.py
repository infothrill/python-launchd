# -*- coding: utf-8 -*-

import subprocess
import plistlib
import six

_LAUNCHCTL_CMD = "launchctl"


def jobs_cmd():
    '''
    Wrapper for `launchctl list`

    Returns a generator for LaunchdJob
    '''
    if six.PY2:
        stdout = launchctl("list")
    else:
        stdout = launchctl("list").decode("utf-8")
    # PID, Status, Label
    lines = iter(stdout.splitlines())
    # skip first line
    next(lines)
    sep = "\t"
    Ox = "0x"
    for line in lines:
        pid, _, last = line.strip().partition(sep)
        status, _, label = last.strip().partition(sep)
        if label.startswith(Ox):
            continue
        if pid.isdigit():
            pid = int(pid)
        else:
            pid = None
        if status.isdigit():
            status = int(status)
        else:
            status = None
        yield LaunchdJob(label, pid, status)


def job_properties_cmd(joblabel):
    '''
    Wrapper for `launchctl -x LABEL`

    Returns dictionary
    :param job: string label or LaunchdJob
    '''
    if six.PY2:
        return dict(plistlib.readPlistFromString(launchctl("list", "-x", joblabel.encode("utf-8"))))
    else:
        return dict(plistlib.readPlistFromBytes(launchctl("list", "-x", joblabel)))


def launchctl(subcommand, *args):
    '''
    A minimal wrapper to call the launchctl binary and capture the output
    :param subcommand: string
    '''
    if isinstance(subcommand, six.text_type):
        subcommand = subcommand.encode('utf-8')
    else:
        raise ValueError("Argument is invalid: %r" % repr(subcommand))
    cmd = [_LAUNCHCTL_CMD, subcommand]
    for arg in args:
        if isinstance(arg, six.text_type):
            cmd.append(arg.encode('utf-8'))
        else:
            raise ValueError("Argument is invalid: %r" % repr(arg))
    output = subprocess.check_output(cmd, stdin=None, stderr=subprocess.STDOUT, shell=False)
    return output
