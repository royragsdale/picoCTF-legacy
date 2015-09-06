from flask import Flask, request, session, send_from_directory, render_template
from flask import Blueprint
import api

from api.common import WebSuccess, WebError
from api.annotations import api_wrapper, require_login, require_teacher, require_admin
from api.annotations import log_action

blueprint = Blueprint("admin_api", __name__)

@blueprint.route('/problems', methods=['GET'])
@api_wrapper
@require_admin
def get_problem_data_hook():
    data = {
        "problems": api.problem.get_all_problems(show_disabled=True),
        "bundles": api.problem.get_all_bundles()
    }
    return WebSuccess(data=data)

@blueprint.route('/users', methods=['GET'])
@api_wrapper
@require_admin
def get_all_users_hook():
    users = api.user.get_all_users()
    if users is None:
        return WebError("There was an error query users from the database.")
    return WebSuccess(data=users)

@blueprint.route('/exceptions', methods=['GET'])
@api_wrapper
@require_admin
def get_exceptions_hook():
    try:
        limit = abs(int(request.args.get("limit")))
        exceptions = api.admin.get_api_exceptions(result_limit=limit)
        return WebSuccess(data=exceptions)

    except (ValueError, TypeError):
        return WebError("limit is not a valid integer.")

@blueprint.route("/problems/submissions", methods=["GET"])
@api_wrapper
@require_admin
def get_problem():
    submission_data = {p["name"]:api.stats.get_problem_submission_stats(pid=p["pid"]) \
                       for p in api.problem.get_all_problems(show_disabled=True)}
    return WebSuccess(data=submission_data)

@blueprint.route("/problems/availability", methods=["POST"])
@api_wrapper
@require_admin
def change_problem_availability_hook():
    pid = request.form.get("pid", None)
    desired_state = request.form.get("state", None)

    state = None

    # This feels really bad. Why doesn't Flask serialize it to the correct type?
    if desired_state == "true":
        state = True
    elif desired_state == "false":
        state = False
    else:
        return WebError("Problems are either enabled or disabled.")

    api.admin.set_problem_availability(pid, state)
    return WebSuccess(data="Problem state changed successfully.")


@blueprint.route("/shell_servers", methods=["GET"])
@api_wrapper
@require_admin
def get_shell_servers():
    return WebSuccess(data=api.shell_servers.get_servers())

@blueprint.route("/shell_servers/add", methods=["POST"])
@api_wrapper
@require_admin
def add_shell_server():
    params = api.common.flat_multi(request.form)
    api.shell_servers.add_server(params)
    return WebSuccess("Shell server added.")

@blueprint.route("/shell_servers/update", methods=["POST"])
@api_wrapper
@require_admin
def update_shell_server():
    params = api.common.flat_multi(request.form)

    sid = params.get("sid", None)
    if sid is None:
        return WebError("Must specify sid to be updated")

    api.shell_servers.update_server(sid, params)
    return WebSuccess("Shell server updated.")

@blueprint.route("/shell_servers/remove", methods=["POST"])
@api_wrapper
@require_admin
def remove_shell_server():
    sid = request.form.get("sid", None)
    if sid is None:
        return WebError("Must specify sid to be removed")

    api.shell_servers.remove_server(sid)
    return WebSuccess("Shell server removed.")

@blueprint.route("/shell_servers/load_problems", methods=["POST"])
@api_wrapper
@require_admin
def load_problems_from_shell_server():
    sid = request.form.get("sid", None)

    if sid is None:
        return WebError("Must provide sid to load from.")

    number = api.shell_servers.load_problems_from_server(sid)
    return WebSuccess("Loaded {} problems from the server".format(number))

@blueprint.route("/shell_servers/check_status", methods=["GET"])
@api_wrapper
@require_admin
def check_status_of_shell_server():
    sid = request.args.get("sid", None)

    if sid is None:
        return WebError("Must provide sid to load from.")

    all_online, data = api.shell_servers.get_problem_status_from_server(sid)

    if all_online:
        return WebSuccess("All problems are online", data=data)
    else:
        return WebError("One or more problems are offline. Please connect and fix the errors.", data=data)

@blueprint.route("/bundle/dependencies_active", methods=["POST"])
@api_wrapper
@require_admin
def bundle_dependencies():
    bid = request.form.get("bid", None)
    state = request.form.get("state", None)

    if bid is None:
        return WebError("Must provide bid to load from.")

    if state is None:
        return WebError("Must provide a state to set.")

    if state == "true":
        state = True
    elif state == "false":
        state = False

    api.problem.set_bundle_dependencies_enabled(bid, state)

    return WebSuccess("Dependencies are now {}.".format("enabled" if state else "disabled"))
