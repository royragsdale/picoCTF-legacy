#!/usr/bin/python3

import api
import spur
import time
from os.path import join

def cache(f, *args, **kwargs):
    result = f(cache=False, *args, **kwargs)
    key = api.cache.get_mongo_key(f, *args, **kwargs)
    api.cache.set(key, result)
    return result

class CantConnectException(Exception):
    pass

# open shell server connections
connections = {}

def get_connection(sid):
    global connections
    if connections.get(sid, None) == None:
        try:
            connections[sid] = api.shell_servers.get_connection(sid)
        except api.common.WebException as e:
            raise CantConnectException
    return connections[sid]

def get_home_dir(shell, user):
    # first make sure the user has an account
    if shell.run(["id", "-u", user], allow_error=True).return_code != 0:
        return None

    home_dir = shell.run(["bash", "-c", "echo ~%s" % user]).output.decode("utf-8").strip()

    return home_dir

@api.cache.memoize()
def get_symlinks(sid, user):
    shell = get_connection(sid)

    home_dir = get_home_dir(shell, user)
    if home_dir == None:
        return None

    problems_path = join(home_dir, "problems")
    try:
        result = shell.run(["sudo", "ls", problems_path]).output.decode("utf-8")
        return result.split("\n")[:-1]
    except spur.results.RunProcessError as e:
        # directory must not exist
        result = shell.run(["sudo", "mkdir", problems_path], allow_error=True)
        if result.return_code != 0:
            # something else is wrong, so give up
            return None

        # try again
        get_symlinks(shell, user)

def rm_symlinks(sid, user, to_remove):
    shell = get_connection(sid)

    home_dir = get_home_dir(shell, user)
    if home_dir == None:
        return None

    problems_path = join(home_dir, "problems")
    for name in to_remove:
        symlink = join(problems_path, name)
        try:
            shell.run(["sudo", "rm", symlink])
            print("Removed symlink %s" % symlink)
        except spur.results.RunProcessError as e:
            print("Failed to remove symlink %s" % symlink)

def add_symlinks(sid, user, to_add):
    shell = get_connection(sid)

    home_dir = get_home_dir(shell, user)
    if home_dir == None:
        return None

    problems_path = join(home_dir, "problems")
    for name, path in to_add.items():
        symlink = join(problems_path, name)
        try:
            shell.run(["sudo", "ln", "-s", path, symlink])
            print("Added symlink %s --> %s" % (symlink, path))
        except spur.results.RunProcessError as e:
            print("Failed to add symlink %s --> %s" % (symlink, path))

def run():
    global connections

    teams = api.team.get_all_teams(show_ineligible=True)

    for server in api.shell_servers.get_servers():

        try:
            for team in teams:
                unlocked_problems = api.problem.get_unlocked_problems(tid=team["tid"])
                correct_symlinks = {p["name"]:p["deployment_directory"] for p in unlocked_problems if p["should_symlink"]}
                correct_names = set(correct_symlinks.keys())

                for user in api.team.get_team_members(tid=team["tid"]):
                    start = time.time()
                    current_symlinks = get_symlinks(server["sid"], user["username"])
                    if current_symlinks == None:
                        continue

                    symlinked_names = set(current_symlinks)
                    to_add = correct_names - symlinked_names
                    to_remove = symlinked_names - correct_names

                    if len(to_add) > 0:
                        add_symlinks(server["sid"], user["username"], {name:correct_symlinks[name] for name in to_add})
                    if len(to_remove) > 0:
                        rm_symlinks(server["sid"], user["username"], to_remove)

                    if len(to_add) > 0 or len(to_remove) > 0:
                        cache(get_symlinks, server["sid"], user["username"])

                    print("Took %.2f seconds." % (time.time() - start))

        except CantConnectException as e:
            print("Couldn't connect to server \"%s\"" % server["name"])

        connections[server["sid"]] = None
