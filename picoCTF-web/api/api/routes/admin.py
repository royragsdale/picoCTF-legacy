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
def get_all_problems_hook():
    problems = api.problem.get_all_problems(show_disabled=True)
    if problems is None:
        return WebError("There was an error querying problems from the database.")
    return WebSuccess(data=problems)

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

@blueprint.route('/flag_sharing', methods=['GET'])
@api_wrapper
@require_admin
def get_flag_shares():
    return WebSuccess(data=api.stats.check_invalid_instance_submissions())

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
