#!/usr/bin/python3

import api
import spur
import json
import string
import random

from os.path import join

script = \
"""
import json
import os
import stat
import pwd
import subprocess

from os.path import join

data = json.loads(raw_input())

for user, symlinks in data.items():
    home_dir = pwd.getpwnam(user).pw_dir
    problems_path = join(home_dir, "problems")

    if not os.path.isdir(problems_path):
        if os.path.isfile(problems_path) or os.path.islink(problems_path):
            os.unlink(problems_path)
            print("Deleted %s because it was not a directory" % problems_path)
        os.mkdir(problems_path)
        print("Made new directory %s" % problems_path)

    dirstat = os.stat(problems_path)

    # if only os.chattr() existed... but I guess the following hacks work

    #if not dirstat.st_mode & stat.UF_NOUNLINK:
    #    os.lchflags(problems_path, dirstat.st_flags | os.SF_NOUNLINK)

    if b"-u-" not in subprocess.check_output(["lsattr", "-d", problems_path]):
        subprocess.check_output(["chattr", "+u", problems_path])
        print("Made %s undeletable." % problems_path)

    if not (dirstat.st_uid == 0 and dirstat.st_gid == 0):
        os.chown(problems_path, 0, 0)
        print("Made %s owned by root:root" % problems_path)

    current_symlinks = set(list(os.listdir(problems_path)))
    correct_symlinks = set(symlinks.keys())

    for problem in correct_symlinks - current_symlinks:
        src, dst = symlinks[problem], join(problems_path, problem)
        os.symlink(src, dst)
        print("Added symlink %s --> %s" % (dst, src))

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
        try:
            with shell.open(script_path, "w") as remote_script:
                remote_script.write(script)
        except Exception as e:
            print("Couldn't open script file")
            continue

        try:
            process = shell.spawn(["sudo", "python", script_path])
            process.stdin_write(json.dumps(data)+"\n")
            result = process.wait_for_result()
            output = result.output.decode('utf-8')
            if output == "":
                print("Everthing up to date")
            else:
                print(output)
        except api.common.WebException as e:
            print("Couldn't run script to create symlinks")

        try:
            shell.run(["sudo", "rm", "-r", temp_dir])
        except api.common.WebException as e:
            print("Couldn't remove temporary directory on shell server")
        except Exception as e:
            print("Unknown error.")
