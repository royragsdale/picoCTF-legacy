""" Module for handling groups of teams """

import api

from voluptuous import Required, Length, Schema
from api.common import check, validate, safe_fail, WebException, InternalException, SevereInternalException

from api.annotations import log_action

register_group_schema = Schema({
    Required("group-name"): check(
        ("Class name must be between 3 and 50 characters.", [str, Length(min=3, max=100)])
    )
}, extra=True)

join_group_schema = Schema({
    Required("group-name"): check(
        ("Class name must be between 3 and 50 characters.", [str, Length(min=3, max=100)]),
    )
}, extra=True)

leave_group_schema = Schema({
    Required("group-name"): check(
        ("Class name must be between 3 and 50 characters.", [str, Length(min=3, max=100)]),
    )
}, extra=True)

delete_group_schema = Schema({
    Required("group-name"): check(
        ("Class name must be between 3 and 50 characters.", [str, Length(min=3, max=100)]),
    )
}, extra=True)

def get_roles_in_group(gid, tid=None, uid=None):
    """
    Determine what role the team plays in a group.

    Args:
        gid: the group id
        tid: the team id
        uid: optional uid
    """

    group = get_group(gid=gid)

    if uid is not None:
        user = api.user.get_user(uid=uid)

        if user["admin"]:
            return {
                "owner": True,
                "teacher": True,
                "member": False
            }
        else:
            # If the user isn't an admin we continue on as normal
            team = api.user.get_team(uid=user["uid"])
    elif tid is not None:
        team = api.team.get_team(tid=tid)
    else:
        raise InternalException("Either tid or uid must be specified to determine role in group.")

    roles = {}
    roles["owner"] = team["tid"] == group["owner"]
    roles["teacher"] = roles["owner"] or team["tid"] in group["teachers"]
    roles["member"] = team["tid"] in group["members"]

    return roles

def get_group(gid=None, name=None, owner_tid=None):
    """
    Retrieve a group based on its name or gid.

    Args:
        name: the name of the group
        gid: the gid of the group
        owner_tid: the tid of the group owner
    Returns:
        The group object.
    """

    db = api.common.get_conn()

    match = {}
    if name is not None and owner_tid is not None:
        match.update({"name": name})
        match.update({"owner": owner_tid})
    elif gid is not None:
        match.update({"gid": gid})
    else:
        raise InternalException("Group name and owner or gid must be specified to look up a group.")

    group = db.groups.find_one(match, {"_id": 0})
    if group is None:
        raise InternalException("Could not find that group!")

    return group

def get_teacher_information(gid):
    """
    Retrieves the team information for all teams in a group.

    Args:
        gid: the group id
    Returns:
        A list of team information
    """

    group = get_group(gid=gid)

    member_information = []
    for tid in group["teachers"]:
        team_information = api.team.get_team_information(tid=tid)
        team_information["teacher"] = True
        member_information.append(team_information)

    return member_information

def get_member_information(gid):
    """
    Retrieves the team information for all teams in a group.

    Args:
        gid: the group id
    Returns:
        A list of team information
    """

    group = get_group(gid=gid)

    member_information = []
    for tid in group["members"]:
        team = api.team.get_team(tid=tid)
        if team["size"] > 0:
            member_information.append(api.team.get_team_information(tid=team["tid"]))

    return member_information

@log_action
def create_group(tid, group_name):
    """
    Inserts group into the db. Assumes everything is validated.

    Args:
        tid: The id of the team creating the group.
        group_name: The name of the group.
    Returns:
        The new group's gid.
    """

    db = api.common.get_conn()

    gid = api.common.token()

    db.groups.insert({
        "name": group_name,
        "owner": tid,
        "teachers": [],
        "members": [],
        "settings": {
          "email_filter": []
        },
        "gid": gid
    })

    return gid

def get_group_settings(gid):
    """
    Get various group settings.
    """

    db = api.common.get_conn()

    #Ensure it exists.
    group = api.group.get_group(gid=gid)
    group_result = db.groups.find_one({"gid": group["gid"]}, {"_id": 0, "settings": 1})

    return group_result["settings"]

def change_group_settings(gid, settings):
    """
    Replace the current settings with the supplied ones.
    """

    db = api.common.get_conn()

    group = api.group.get_group(gid=gid)
    db.groups.update({"gid": group["gid"]}, {"$set": {"settings": settings}})


@log_action
def join_group(tid, gid, teacher=False):
    """
    Adds a team to a group. Assumes everything is valid.

    Args:
        tid: the team id
        gid: the group id to join
        teacher: whether or not the user is a teacher
    """

    db = api.common.get_conn()

    role_group = "teachers" if teacher else "members"

    if teacher:
        uids = api.team.get_team_uids(tid=tid)
        for uid in uids:
            api.admin.give_teacher_role(uid=uid)

    db.groups.update({'gid': gid}, {'$push': {role_group: tid}})

def join_group_request(params, tid=None):
    """
    Tries to place a team into a group. Validates forms.
    All required arguments are assumed to be keys in params.

    Args:
        group-name: The name of the group to join.
        group-owner: The name of the owner of the group
        Optional:
            tid: If omitted,the tid will be grabbed from the logged in user.
    """


    validate(join_group_schema, params)
    owner_uid = api.user.get_user(name=params["group-owner"])["uid"]
    if safe_fail(get_group, name=params["group-name"], owner_uid=owner_uid) is None:
        raise WebException("No class exists with that name!")

    group = get_group(name=params["group-name"], owner_uid=owner_uid)

    #TODO: assumes teams of size 1
    user = api.user.get_user()

    if tid is None:
        tid = user["tid"]

    group_settings = get_group_settings(gid=group["gid"])

    if not api.user.verify_email_in_whitelist(user["email"], group_settings["email_filter"]):
        raise WebException("Your email does not belong to the whitelist for that group. You may not join it yourself.")

    if tid in group['members'] or tid in group["teachers"]:
        raise WebException("Your team is already a member of that class!")

    join_group(tid, group["gid"])

def sync_teacher_status(tid, uid):
    """
    Determine if the given user is still a teacher and update his status.
    """

    db = api.common.get_conn()

    active_teacher_roles = db.groups.find({"$or": [{"teachers": tid}, {"owner": uid}]}).count()
    db.users.update({"uid": uid}, {"$set": {"teacher": active_teacher_roles > 0}})

@log_action
def leave_group(gid, tid=None, uid=None):
    """
    Removes a team from a group

    Args:
        tid: the team id
        gid: the group id to leave
    """

    db = api.common.get_conn()

    group = get_group(gid=gid)
    team = api.team.get_team(tid=tid)

    roles = get_roles_in_group(gid, tid=team["tid"],)

    role = "members"
    if is_member_of_group(gid=group["gid"], tid=team["tid"]):
        role = "members"
    elif is_teacher_of_group(gid=group["gid"], tid=team["tid"]):
        role = "teachers"
    elif is_owner_of_group(gid=group["gid"], tid=team["tid"]):
        raise InternalException("Owners can not leave their group.")
    else:
        raise InternalException("That team does not belong to that group.")

    db.groups.update({'gid': gid}, {'$pull': {role: tid}})

    #TODO: only works with team size of 1.
    if team["size"] == 1:
        uid = api.team.get_team_uids(tid=tid)[0]
        sync_teacher_status(tid, uid)

def leave_group_request(params, tid=None):
    """
    Tries to remove a team from a group. Validates forms.
    All required arguments are assumed to be keys in params.

    Args:
        group-name: The name of the group to leave.
        group-owner: The owner of the group to leave.
        Optional:
            tid: If omitted,the tid will be grabbed from the logged in user.
    """

    validate(leave_group_schema, params)
    owner_uid = api.user.get_user(name=params["group-owner"])["uid"]
    group = get_group(name=params["group-name"], owner_uid=owner_uid)

    if tid is None:
        tid = api.user.get_team()["tid"]

    if tid not in group['members']:
        raise WebException("Your team is not a member of that class!")

    leave_group(tid, group["gid"])

def switch_role(gid, uid, role):
    """
    Switch a user's given role in his group.

    Cannot switch to/from owner.
    """

    db = api.common.get_conn()

    group = get_group(gid=gid)
    user = api.user.get_user(uid=uid)
    tid = api.user.get_team(uid=user["uid"])["tid"]

    if role == "member":
        if api.group.is_teacher_of_group(gid=gid, tid=tid) and not api.group.is_member_of_group(gid=gid, tid=tid):
            db.groups.update({"gid": gid}, {"$pull": {"teachers": tid}, "$push": {"members": tid}})
        else:
            raise InternalException("User is already a member of that group.")

    elif role == "teacher":
        if not api.group.is_teacher_of_group(gid=gid, tid=tid) and api.group.is_member_of_group(gid=gid, tid=tid):
            db.groups.update({"gid": gid}, {"$push": {"teachers": tid}, "$pull": {"members": tid}})
        else:
            raise InternalException("User is already a teacher of that group.")

    else:
        raise InternalException("Only supported roles are member and teacher.")

    #Keep teacher status up to date.
    sync_teacher_status(tid, uid)

@log_action
def delete_group(gid):
    """
    Deletes a group

    Args:
        gid: the group id to delete
    """

    db = api.common.get_conn()

    db.groups.remove({'gid': gid})

def delete_group_request(params, uid=None):
    """
    Tries to delete a group. Validates forms.
    All required arguments are assumed to be keys in params.

    Args:
        group-name: The name of the group to join.
        Optional:
            uid: If omitted, the uid will be grabbed from the logged in user.
    """

    validate(delete_group_schema, params)

    if uid is None:
        uid = api.user.get_user()['uid']

    if safe_fail(get_group, name=params['group-name'], owner_uid=uid) is None:
        raise WebException("No class exists with that name!")

    if uid is None:
        uid = api.user.get_user()["uid"]

    group = get_group(name=params["group-name"], owner_uid=uid)

    delete_group(group['gid'])


def get_all_groups():
    """
    Returns a list of all groups in the database.
    """

    db = api.common.get_conn()

    return list(db.groups.find({}, {"_id": 0}))
