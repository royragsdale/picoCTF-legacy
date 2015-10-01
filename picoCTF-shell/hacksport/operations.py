"""
Low level deployment operations.
"""

from random import randint, Random
from os import path, makedirs
from spur import LocalShell
from time import time
from signal import SIGTERM
from hashlib import md5

class TimeoutError(Exception):
    """
    Exception dealing with executed commands that timeout.
    """
    pass

def execute(cmd, timeout=5, **kwargs):
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

def create_user(username, home_directory_root="/home/", obfuscate=True):
    """
    Creates a user with the given username

    Args:
        username: the username to create
        home_directory_root: the parent directory to create the
                             home directory in. Defaults to /home/

    Returns:
        The new user's home directory
    """

    directory_name = username

    if obfuscate:
        directory_name += md5(username.encode()).hexdigest()

    home_directory = path.join(home_directory_root, directory_name)

    if not path.isdir(home_directory):
        makedirs(home_directory)

    execute(["useradd", "-s", "/bin/bash", "-m", "-d", home_directory, username])

    return home_directory
