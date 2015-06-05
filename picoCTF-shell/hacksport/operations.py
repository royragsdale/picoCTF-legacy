"""
Low level deployment operations.
"""

from random import randint
from os import system, path, setsid, killpg
from signal import SIGTERM
from subprocess import Popen, PIPE

def give_port():
    """
    Returns a random port and registers it.
    """
    #TODO: handle registering ports
    return randint(1000, 65000)

def exec_cmd(cmd):
    """
    Executes the given shell command

    Args:
        cmd: the shell command to run
    Returns:
        A tuple containing stdout_output, stderr_output
    """

    process = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE, preexec_fn=setsid)
    stdout, stderr = process.stdout.read(), process.stderr.read()
    killpg(process.pid, SIGTERM)
    return stdout, stderr

def create_user(username, home_directory_root="/home/"):
    """
    Creates a user with the given username

    Args:
        username: the username to create
        home_directory_root: the parent directory to create the
                             home directory in. Defaults to /home/

    Returns:
        The new user's home directory
    """

    home_directory = path.join(home_directory_root, username)

    cmd = "useradd -m -d {} {}".format(home_directory, username)
    exec_cmd(cmd)
    return home_directory
