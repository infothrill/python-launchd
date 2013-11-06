# -*- coding: utf-8 -*-

import subprocess

import six


def launchctl(subcommand, *args):
    '''
    A minimal wrapper to call the launchctl binary and capture the output
    :param subcommand: string
    '''
    if not isinstance(subcommand, six.string_types):
        raise ValueError("Argument is invalid: %r" % repr(subcommand))
    if isinstance(subcommand, six.text_type):
        subcommand = subcommand.encode('utf-8')

    cmd = ["launchctl", subcommand]
    for arg in args:
        if isinstance(arg, six.string_types):
            if isinstance(arg, six.text_type):
                cmd.append(arg.encode('utf-8'))
            else:
                cmd.append(arg)
        else:
            raise ValueError("Argument is invalid: %r" % repr(arg))
    return subprocess.check_output(cmd, stdin=None, stderr=subprocess.STDOUT, shell=False)
