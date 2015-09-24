from flask import Flask, request, session, send_from_directory, render_template
from flask import Blueprint
import api, json

from api.common import WebSuccess, WebError
from api.annotations import api_wrapper, require_login, require_teacher, require_admin, check_csrf
from api.annotations import block_before_competition, block_after_competition
from api.annotations import log_action

blueprint = Blueprint("group_api", __name__)

@blueprint.route('', methods=['GET'])
@api_wrapper
@require_login
def get_group_hook():
    name = request.form.get("group-name")
    owner = request.form.get("group-owner")
    gid = request.form.get("gid")

    owner_uid = api.user.get_user(name=owner)["uid"]

    if gid is not None:
        if not api.group.is_member_of_group(gid=gid):
            return WebError("You are not a member of this group.")
    else:
        if not api.group.is_member_of_group(name=name, owner_uid=owner_uid):
            return WebError("You are not a member of this group.")

    return WebSuccess(data=api.group.get_group(name=request.form.get("group-name"), owner_uid=owner_uid))

@blueprint.route('/settings', methods=['GET'])
@api_wrapper
def get_group_settings_hook():
    gid = request.args.get("gid")
    group = api.group.get_group(gid=gid)

    prepared_data = {
        "name": group["name"],
        "settings": api.group.get_group_settings(gid=group["gid"])
    }

    return WebSuccess(data=prepared_data)

@blueprint.route('/settings', methods=['POST'])
@api_wrapper
@require_teacher
def change_group_settings_hook():
    gid = request.form.get("gid")
    settings = json.loads(request.form.get("settings"))

    user = api.user.get_user()
    group = api.group.get_group(gid=gid)

    if api.group.is_teacher_of_group(uid=user["uid"], gid=group["gid"]):
        api.group.change_group_settings(group["gid"], settings)
        return WebSuccess(message="Group settings changed successfully.")
    else:
        return WebError(message="You do not have sufficient privilege to do that.")

@blueprint.route('/invite', methods=['POST'])
@api_wrapper
@require_teacher
def invite_email_to_group_hook():
    gid = request.form.get("gid")
    email = request.form.get("email")
    role = request.form.get("role")

    user = api.user.get_user()

    if gid is None or email is None or len(email) == 0:
        return WebError(message="You must specify a gid and email address to invite.")

    if role not in ["member", "teacher"]:
        return WebError(message="A user's role is either a member or teacher.")

    group = api.group.get_group(gid=gid)

    if api.group.is_teacher_of_group(uid=user["uid"], gid=group["gid"]) or api.group.is_teacher_of_group(uid=user["uid"], gid=group["gid"]):
        api.email.send_email_invite(group["gid"], email, teacher=(role == "teacher"))
        return WebSuccess(message="Email invitation has been sent.")
    else:
        return WebError(message="You do not have sufficient privilege to do that.")

@blueprint.route('/list')
@api_wrapper
@require_login
def get_group_list_hook():
    return WebSuccess(data=api.team.get_groups())

@blueprint.route('/teacher_information', methods=['GET'])
@api_wrapper
@require_teacher
def get_teacher_information_hook(gid=None):
    gid = request.args.get("gid")
    if not api.group.is_teacher_of_group(gid=gid):
        return WebError("You are not a teacher for this group.")

    return WebSuccess(data=api.group.get_teacher_information(gid=gid))

@blueprint.route('/member_information', methods=['GET'])
@api_wrapper
@require_teacher
def get_memeber_information_hook(gid=None):
    gid = request.args.get("gid")
    if not api.group.is_teacher_of_group(gid=gid):
        return WebError("You are not a teacher for this group.")

    return WebSuccess(data=api.group.get_member_information(gid=gid))

@blueprint.route('/score', methods=['GET'])
@api_wrapper
@require_teacher
def get_group_score_hook():  #JB: Fix this
    name = request.args.get("group-name")
    if not api.group.is_teacher_of_group(gid=name):
        return WebError("You do not own that group!")

    #TODO: Investigate!
    score = api.stats.get_group_scores(name=name)
    if score is None:
        return WebError("There was an error retrieving your score.")

    return WebSuccess(data={'score': score})

@blueprint.route('/create', methods=['POST'])
@api_wrapper
@check_csrf
@require_admin
def create_group_hook():
    gid = api.group.create_group_request(api.common.flat_multi(request.form))
    return WebSuccess("Successfully created group", gid)

@blueprint.route('/join', methods=['POST'])
@api_wrapper
@check_csrf
@require_login
def join_group_hook():
    api.group.join_group_request(api.common.flat_multi(request.form))
    return WebSuccess("Successfully joined group")

@blueprint.route('/leave', methods=['POST'])
@api_wrapper
@check_csrf
@require_login
def leave_group_hook():
    api.group.leave_group_request(api.common.flat_multi(request.form))
    return WebSuccess("Successfully left group")

@blueprint.route('/delete', methods=['POST'])
@api_wrapper
@check_csrf
@require_admin
def delete_group_hook():
    api.group.delete_group_request(api.common.flat_multi(request.form))
    return WebSuccess("Successfully deleted group")

@blueprint.route('/flag_sharing', methods=['GET'])
@api_wrapper
@require_teacher
def get_flag_shares():
    gid = request.args.get("gid", None)
    if gid is None:
        return WebError("You must specify a gid")
    else:
        if not api.group.is_teacher_of_group(gid=gid):
            return WebError("You must own a group to see its flag sharing statistics.")

    return WebSuccess(data=api.stats.check_invalid_instance_submissions(gid=gid))

@blueprint.route('/teacher/leave', methods=['POST'])
@api_wrapper
@check_csrf
@require_teacher
def force_leave_group_hook():
    gid = request.form.get("gid")
    tid = request.form.get("tid")

    if gid is None or tid is None:
        return WebError("You must specify a gid and tid.")

    api.group.leave_group(tid, gid)

    return WebSuccess("Team has successfully left the group.")

@blueprint.route('/teacher/role_switch', methods=['POST'])
@api_wrapper
@require_teacher
def switch_user_role_group_hook():
    gid = request.form.get("gid")
    uid = request.form.get("uid")
    role = request.form.get("role")

    user = api.user.get_user()

    if gid is None or uid is None:
        return WebError(message="You must specify a gid and uid to perform a role switch.")

    if role not in ["member", "teacher"]:
        return WebError(message="A user's role is either a member or teacher.")

    group = api.group.get_group(gid=gid)

    if api.group.is_owner_of_group(uid=user["uid"], gid=group["gid"]) or api.group.is_teacher_of_group(uid=user["uid"], gid=group["gid"]):
        affected_user = api.user.get_user(uid=uid)

        if api.group.is_owner_of_group(uid=affected_user["uid"], gid=group["gid"]):
            return WebError(message="You can not change the role of the owner of the group.")

        api.group.switch_role(group["gid"], affected_user["uid"], role)
        return WebSuccess(message="User's role has been successfully changed.")
    else:
        return WebError(message="You do not have sufficient privilege to do that.")
