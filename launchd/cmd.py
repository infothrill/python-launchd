# -*- coding: utf-8 -*-

import subprocess

_LAUNCHCTL_CMD = "launchctl"


def launchctl(subcommand, *args):
    '''
    A minimal wrapper to call the launchctl binary and capture the output
    :param subcommand: string
    '''
    if not isinstance(subcommand, str):
        raise ValueError("Argument is invalid: %r" % repr(subcommand))
    cmd = [_LAUNCHCTL_CMD, subcommand]
    for arg in args:
        if isinstance(arg, str):
            cmd.append(arg)
        else:
            raise ValueError("Argument is invalid: %r" % repr(arg))
    output = subprocess.check_output(cmd, stdin=None, stderr=subprocess.STDOUT, shell=False)
    return output
