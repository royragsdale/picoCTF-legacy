"""
API functions relating to admin users.
"""

import api

from api.common import check, validate, safe_fail
from api.common import WebException, InternalException
from api.annotations import log_action

def give_admin_role(name=None, uid=None):
    db = api.common.get_conn()

    user = api.user.get_user(name=name, uid=uid)
    db.users.update({"uid": user["uid"]}, {"$set": {"admin": True}})

def set_problem_availability(pid, enabled):
    """
    Updates a problem's availability.

    Args:
        pid: the problem's pid
        disabled: whether or not the problem should be disabled.
    Returns:
        The updated problem object.
    """

    return api.problem.update_problem(pid, {"disabled": not(enabled)})
