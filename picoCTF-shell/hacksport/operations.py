"""
Low level deployment operations.
"""

from random import randint, Random
from os import path, makedirs
from spur import LocalShell
from time import time
from signal import SIGTERM

from hacksport.deploy import get_deploy_context

port_random = None

def give_port():
    """
    Returns a random port and registers it.
    """

    global port_random

    context = get_deploy_context()

    # default behavior
    if context["config"] is None:
        return randint(1000, 65000)

    # during real deployment, let's register a port
    if port_random is None:
        port_random = Random(context["config"].DEPLOY_SECRET)

    if len(context["port_map"].items()) + len(context["config"].BANNED_PORTS) == 65536:
        raise Exception("All usable ports are taken. Cannot deploy any more instances.")

    while True:
        port = port_random.randint(0, 65535)
        if port not in context["config"].BANNED_PORTS:
            owner, instance = context["port_map"].get(port, (None, None))
            if owner is None or (owner is context["problem"] and instance is context["instance"]):
                context["port_map"][port] = (context["problem"], context["instance"])
                return port

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

    execute(["useradd", "-s", "/bin/bash", "-m", "-d", home_directory, username])

    return home_directory
