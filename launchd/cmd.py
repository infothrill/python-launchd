import subprocess  # noqa: S404


def launchctl(subcommand, *args):
    """
    Call the launchctl binary and capture the output.

    :param subcommand: string
    """
    if not isinstance(subcommand, str):
        raise ValueError("Argument is invalid: %r" % repr(subcommand))
    if isinstance(subcommand, str):
        subcommand = subcommand.encode("utf-8")

    cmd = ["launchctl", subcommand]
    for arg in args:
        if isinstance(arg, str):
            if isinstance(arg, str):
                cmd.append(arg.encode("utf-8"))
            else:
                cmd.append(arg)
        else:
            raise ValueError("Argument is invalid: %r" % repr(arg))
    return subprocess.check_output(cmd, stdin=None, stderr=subprocess.STDOUT, shell=False)  # noqa: S603
