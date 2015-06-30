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

    params["sid"] = api.common.token()
    db.shell_servers.insert(params)

def update_server(sid, params):
    """
    Update a shell server from the pool of servers.

    Args:
        sid: The sid of the server to update
        params: A dict containing:
            port
            username
            password
    """

    db = api.common.get_conn()

    if db.shell_servers.find_one({"sid": sid}) is None:
        raise WebException("Shell server with sid '{}' does not exist.".format(sid))

    if isinstance(params["port"], str):
        params["port"] = int(params["port"])

    db.shell_servers.update({"sid": sid}, {"$set": params})

def remove_server(sid):
    """
    Remove a shell server from the pool of servers.

    Args:
        sid: the sid of the server to be removed
    """

    db = api.common.get_conn()

    if db.shell_servers.find_one({"sid": sid}) is None:
        raise WebException("Shell server with sid '{}' does not exist.".format(sid))

    db.shell_servers.remove({"sid": sid})

def get_server(sid):
    """
    Returns the server object corresponding to the sid provided

    Args:
        sid: the server id to lookup

    Returns:
        The server object
    """

    db = api.common.get_conn()
    server = db.shell_servers.find_one({"sid": sid})
    if server is None:
        raise WebException("Server with sid '{}' does not exist".format(sid))

    return server

def get_servers():
    """
    Returns the list of added shell servers.
    """

    db = api.common.get_conn()
    return list(db.shell_servers.find({}, {"_id": 0}))

def get_problem_status_from_server(sid):
    """
    Connects to the server and checks the status of the problems running there.
    Runs `sudo shell_manager status --json` and parses its output.

    Args:
        sid: The sid of the server to check

    Returns:
        A tuple containing:
            - True if all problems are online and false otherwise
            - A list of errors (dictionaries containing "problem", "instance", "type")
    """

    server = get_server(sid)
    shell = get_connection(server['host'], server['port'], server['username'], server['password'])

    output = shell.run(["sudo", "shell_manager", "status", "--json"]).output.decode("utf-8")
    data = json.loads(output)

    errors = []
    for problem in data["problems"]:
        for instance in problem["instances"]:
            # if the service is not working
            if not instance["service"]:
                errors.append({
                    "problem": problem["name"],
                    "instance": instance["iid"],
                    "type": "service"
                })

            # if the connection is not working and it is a remote challenge
            if not instance["connection"] and instance["port"] is not None:
                errors.append({
                    "problem": problem["name"],
                    "instance": instance["iid"],
                    "type": "connection"
                })

    return (len(errors) == 0, errors)

def load_problems_from_server(sid):
    """
    Connects to the server and loads the problems from its deployment state.
    Runs `sudo shell_manager publish` and captures its output.

    Args:
        sid: The sid of the server to load problems from.
    """

    server = get_server(sid)
    shell = get_connection(server['host'], server['port'], server['username'], server['password'])

    result = shell.run(["sudo", "shell_manager", "publish"])
    data = json.loads(result.output.decode("utf-8"))
    api.problem.load_published(data)
