#!/usr/bin/python3

import api
import spur
import json
import string
import random

from os.path import join

script = """
import json
import os
import pwd

from os.path import join

data = json.loads(raw_input())

for user, symlinks in data.items():
    home_dir = pwd.getpwnam(user).pw_dir
    problems_path = join(home_dir, "problems")

    if not os.path.isdir(problems_path):
        os.mkdir(problems_path)
        os.chown(problems_path, 0, 0)

    current_symlinks = set(list(os.listdir(problems_path)))
    correct_symlinks = set(symlinks.keys())

    for problem in correct_symlinks - current_symlinks:
        src, dst = symlinks[problem], join(problems_path, problem)
        os.symlink(src, dst)
        print("Added symlink %s --> %s" % (src, dst))

    for problem in current_symlinks - correct_symlinks:
        link = join(problems_path, problem)
        assert os.path.islink(link), "%s is not a symlink!" % link
        os.unlink(link)
        print("Removed symlink %s" % link)
"""

def make_temp_dir(shell):
    path = "".join(random.choice(string.ascii_lowercase) for i in range(10))

    full_path = join("/tmp", path)

    try:
        shell.run(["mkdir", full_path])
        return full_path
    except api.common.WebException as e:
        return None

def run():
    global connections

    teams = api.team.get_all_teams(show_ineligible=True)

    for server in api.shell_servers.get_servers():
        try:
            shell = api.shell_servers.get_connection(server["sid"])
        except api.common.WebException as e:
            print("Can't connect to server \"%s\"" % server["name"])
            continue

        data = {}
        for team in teams:
            unlocked_problems = api.problem.get_unlocked_problems(tid=team["tid"])
            correct_symlinks = {p["name"]:p["deployment_directory"] for p in unlocked_problems if p["should_symlink"]}

            data.update({user["username"]:correct_symlinks for user in api.team.get_team_members(tid=team["tid"])})

        temp_dir = make_temp_dir(shell)
        if temp_dir == None:
            print("Couldn't make temporary directory on shell server")
            continue

        script_path = join(temp_dir, "symlinker.py")
        with shell.open(script_path, "w") as remote_script:
            remote_script.write(script)

        try:
            process = shell.spawn(["sudo", "python", script_path])
            process.stdin_write(json.dumps(data)+"\n")
            result = process.wait_for_result()
            output = result.output.decode('utf-8')
            if output != "":
                print(output)
        except api.common.WebException as e:
            print("Couldn't run script to create symlinks")

        try:
            shell.run(["sudo", "rm", "-r", temp_dir])
        except api.common.WebException as e:
            print("Couldn't remove temporary directory on shell server")
            continue
