import sys, api
from api.common import safe_fail

SHELL_NAME = "Example Shell"

shell_password = "vagrant" if len(sys.argv) <= 1 else sys.argv[1]

try:
    if safe_fail(api.shell_servers.get_server, name=SHELL_NAME) is None:
        sid = api.shell_servers.add_server({
            "name": SHELL_NAME,
            "host": "192.168.2.3",
            "port": 22,
            "username": "vagrant",
            "password": shell_password,
            "protocol": "HTTP"
        })
except Exception as e:
    print("Failed to connect to shell server.")
    print(e)

try:
    sid = api.shell_servers.get_server(name=SHELL_NAME)["sid"]
    api.shell_servers.load_problems_from_server(sid)
    [api.admin.set_problem_availability(p["pid"], False) for p in api.problem.get_all_problems(show_disabled=True)]
    [api.problem.set_bundle_dependencies_enabled(b["bid"], True) for b in api.problem.get_all_bundles()]
    print("Loaded problems successfully.")
except Exception as e:
    print(e)
    print("Failed to load problems.")
