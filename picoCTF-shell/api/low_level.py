from random import randint
from os import system

def give_port():
    """
    Returns a random port and registers it.
    """
    #TODO: handle registering ports
    return randint(1000, 65000)

def create_user(username, home_directory_root="/home/"):
    """
    Creates a user with the given username

    Args:
        username: the username to create
        home_directory_root: the parent directory to create the
                             home directory in. Defaults to /home/
    """
    #TODO: implement
    pass

def exec_cmd(cmd):
    system(cmd)
