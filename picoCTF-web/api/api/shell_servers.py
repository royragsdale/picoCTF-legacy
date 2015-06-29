import api
import pymongo
import spur
import json

from api.common import WebException

def get_connection(host, port, username, password):
    """
    Attempts to connect to the given server and
    returns a connection.
    """

    try:
        shell = spur.SshShell(
            hostname=host,
            username=username,
            password=password,
            port=port,
            missing_host_key=spur.ssh.MissingHostKey.accept,
            connect_timeout=10
        )
        shell.run(["echo", "connected"])
    except spur.ssh.ConnectionError as e:
        raise WebException("Cannot connect to {}@{}:{} with the specified password".format(username, host, port))

    return shell

def add_server(params):
    """
    Add a shell server to the pool of servers.

    Args:
        params: A dict containing:
            host
            port
            username
            password
    """

    db = api.common.get_conn()

    if isinstance(params["port"], str):
        params["port"] = int(params["port"])

    try:
        db.shell_servers.insert(params)
    except pymongo.errors.DuplicateKeyError as e:
        raise WebException("Host '{}' has already been added.".format(params['host']))

def update_server(host, params):
    """
    Update a shell server from the pool of servers.

    Args:
        host: The host to update
        params: A dict containing:
            port
            username
            password
    """

    db = api.common.get_conn()

    if db.shell_servers.find_one({"host": host}) is None:
        raise WebException("Shell server with host '{}' does not exist.".format(host))

    if isinstance(params["port"], str):
        params["port"] = int(params["port"])

    db.shell_servers.update({"host": host}, {"$set": params})

def remove_server(host):
    """
    Remove a shell server from the pool of servers.

    Args:
        host: the host of the server to be removed
    """

    db = api.common.get_conn()

    if db.shell_servers.find_one({"host": host}) is None:
        raise WebException("Shell server with host '{}' does not exist.".format(host))

    db.shell_servers.remove({"host": host})

def get_servers():
    """
    Returns the list of added shell servers.
    """

    db = api.common.get_conn()
    return list(db.shell_servers.find({}, {"_id": 0}))

def load_problems_from_server(host):
    """
    Connects to the server and loads the problems from its deployment state.
    Runs `sudo shell_manager publish` and captures its output.

    Args:
        host: The host of the server to load problems from.
    """

    db = api.common.get_conn()

    server = db.shell_servers.find_one({"host": host})

    if server is None:
        raise WebException("Server with host '{}' does not exist".format(host))

    shell = get_connection(server['host'], server['port'], server['username'], server['password'])

    result = shell.run(["sudo", "shell_manager", "publish"])
    data = json.loads(result.output.decode("utf-8"))
    api.problem.load_published(data)
