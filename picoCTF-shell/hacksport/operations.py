"""
Low level deployment operations.
"""

from random import randint
from os import path, makedirs
from spur import LocalShell
from time import time
from signal import SIGTERM

def give_port():
    """
    Returns a random port and registers it.
    """
    #TODO: handle registering ports
    return randint(1000, 65000)

class TimeoutError(Exception):
    """
    Exception dealing with executed commands that timeout.
    """
    pass

def execute(cmd, timeout=1, **kwargs):
    """
    Executes the given shell command

    Args:
        cmd: List of command arguments
        timeout: maximum alloted time for the command
        **kwargs: passes to LocalShell.spawn
    Returns:
        An execution result.
    Raises:
        NoSuchCommandError, RunProcessError, FileNotFoundError
    """

    shell = LocalShell()

    #It is unlikely that someone actually intends to supply
    #a string based on how spur works.
    if type(cmd) == str:
        cmd = ["bash", "-c"] + [cmd]

    process = shell.spawn(cmd, store_pid=True, **kwargs)
    start_time = time()

    while process.is_running():
        delta_time = time() - start_time
        if delta_time > timeout:
            process.send_signal(SIGTERM)
            raise TimeoutError(cmd, timeout)

    return process.wait_for_result()

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

    if not path.isdir(home_directory):
        makedirs(home_directory)

    execute(["useradd", "-m", "-d", home_directory, username])

    return home_directory
