#!/usr/bin/python3

# Simple script to programatically add a shell server to a running picoCTF web
# instance.  If using a custom APP_SETTINGS_FILE, ensure the appropriate
# environment variable is set prior to running this script. This script is best
# run from the roles/pico-web/tasks/auto-add-shell.yml playbook

import sys

# The picoCTF api
import api

def main(name, host, user, password, port=22, proto="HTTP"):
    # Add a shell server
    try:
        sid = api.shell_servers.add_server({
            "name":name,
            "host": host,
            "port": port,
            "username": user,
            "password": password,
            "protocol": proto})
    except Exception as e:
        print("Failed to connect to shell server.")
        print(e)
        sys.exit

    # Load problems and bundles from the shell server
    try:
        sid = api.shell_servers.get_server(name=name)["sid"]
        api.shell_servers.load_problems_from_server(sid)
        
        # Set problems to disabled
        for p in api.problem.get_all_problems(show_disabled=True):
            api.admin.set_problem_availability(p["pid"], False)

        # Set bundles to enabled to set correct unlock behavior
        for b in api.problem.get_all_bundles():
            api.problem.set_bundle_dependencies_enabled(b["bid"], True)
        
        print("Loaded problems and bundles successfully.")
    except Exception as e:
        print(e)
        print("Failed to load problems.")
        sys.exit

if __name__ == "__main__":

    num_args = len(sys.argv)-1
    if num_args < 4:
        print("Insfficuent arguments passed, need at least")
        print("name, host, user, password")
        sys.exit
    elif num_args == 4:
        _, name, host, user, password = sys.argv
        main(name, host, user, password)
    elif num_args == 5:
        _, name, host, user, password, port = sys.argv
        main(name, host, user, password, port)
    elif num_args == 6:
        _, name, host, user, password, port, proto = sys.argv
        main(name, host, user, password, port, proto)
    else:
        print("Too many arguments passed, need at most")
        print("name, host, user, password, port, proto")
        print(sys.argv)
        sys.exit
