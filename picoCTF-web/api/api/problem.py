""" Module for interacting with the problems """

import imp
import pymongo

import api

from random import randint
from copy import deepcopy
from datetime import datetime
from api.common import validate, check, safe_fail, InternalException, SevereInternalException, WebException
from voluptuous import Schema, Length, Required, Range
from bson import json_util
from os.path import join, isfile

from api.annotations import log_action

submission_schema = Schema({
    Required("tid"): check(
        ("This does not look like a valid tid.", [str, Length(max=100)])),
    Required("pid"): check(
        ("This does not look like a valid pid.", [str, Length(max=100)])),
    Required("key"): check(
        ("This does not look like a valid key.", [str, Length(max=100)]))
})

problem_schema = Schema({
    Required("name"): check(
        ("The problem's display name must be a string.", [str])),
    Required("score"): check(
        ("Score must be a positive integer.", [int, Range(min=0)])),
    Required("author"): check(
        ("Author must be a string.", [str])),
    Required("category"): check(
        ("Category must be a string.", [str])),
    Required("instances"): check(
        ("The instances must be a list.", [list])),
    "description": check(
        ("The problem description must be a string.", [str])),
    "version": check(
        ("A version must be a string.", [str])),
    "tags": check(
        ("Tags must be described as a list.", [list])),
    "hints": check(
        ("Hints must be a list.", [list])),
    "organization": check(
        ("Organization must be string.", [str])),
    "pkg_architecture": check(
        ("Package architecture must be string.", [str])),
    "pkg_description": check(
        ("Package description must be string.", [str])),
    "pkg_name": check(
        ("Package name must be string.", [str])),
    "pkg_dependencies": check(
        ("Package dependencies must be list.", [list])),
    "pip_requirements": check(
        ("pip requirements must be list.", [list])),
    "pid": check(
        ("You should not specify a pid for a problem.", [lambda _: False])),
    "_id": check(
        ("Your problems should not already have _ids.", [lambda id: False]))
})

instance_schema = Schema({
    Required("description"): check(
        ("The description must be a string.", [str])),
    Required("flag"): check(
        ("The flag must be a string.", [str])),
    Required("iid"): check(
        ("The iid must be an int", [int])),
    "port": check(
        ("The port must be an int", [int])),
    "server": check(
        ("The server must be a string.", [str]))
})

def get_all_categories(show_disabled=False):
    """
    Gets the set of distinct problem categories.

    Args:
        show_disabled: Whether to include categories that are only on disabled problems
    Returns:
        The set of distinct problem categories.
    """

    db = api.common.get_conn()

    match = {}
    if not show_disabled:
        match.update({"disabled": False})

    return db.problems.find(match).distinct("category")

def analyze_problems():
    """
    Checks the sanity of inserted problems.
    Includes weightmap verification.

    Returns:
        A list of error strings describing the problems.
    """

    unknown_weightmap_pid = "{}: Has weightmap entry '{}' which does not exist."

    problems = get_all_problems()

    errors = []

    for problem in problems:
        for pid in problem["weightmap"].keys():
            if safe_fail(get_problem, pid=pid) is None:
                errors.append(unknown_weightmap_pid.format(problem["name"], pid))
    return errors

def insert_problem(problem):
    """
    Inserts a problem into the database. Does sane validation.

    Args:
        Problem dict.
        score: points awarded for completing the problem.
        category: problem's category
        author: author of the problem
        description: description of the problem.

        Optional:
        version: version of the problem
        tags: list of problem tags.
        hints: hints for completing the problem.
        organization: Organization that author is associated with
    Returns:
        The newly created problem id.
    """

    db = api.common.get_conn()
    validate(problem_schema, problem)

    for instance in problem["instances"]:
        validate(instance_schema, instance)

    # initially disable problems
    problem["disabled"] = True
    problem["pid"] = api.common.hash("{}-{}".format(problem["name"], problem["author"]))
    problem["weightmap"] = {}
    problem["threshold"] = 0

    if safe_fail(get_problem, pid=problem["pid"]) is not None:
        raise WebException("Problem with identical pid already exists.")

    if safe_fail(get_problem, name=problem["name"]) is not None:
        raise WebException("Problem with identical name already exists.")

    db.problems.insert(problem)
    api.cache.fast_cache.clear()

    return problem["pid"]

def remove_problem(pid):
    """
    Removes a problem from the given database.

    Args:
        pid: the pid of the problem to remove.
    Returns:
        The removed problem object.
    """

    db = api.common.get_conn()
    problem = get_problem(pid=pid)

    db.problems.remove({"pid": pid})
    api.cache.fast_cache.clear()

    return problem

def update_problem(pid, updated_problem):
    """
    Updates a problem with new properties.

    Args:
        pid: the pid of the problem to update.
        updated_problem: an updated problem object.
    Returns:
        The updated problem object.
    """

    db = api.common.get_conn()

    if updated_problem.get("name", None) is not None:
        if safe_fail(get_problem, name=updated_problem["name"]) is not None:
            raise WebException("Problem with identical name already exists.")

    problem = get_problem(pid=pid, show_disabled=True).copy()
    problem.update(updated_problem)

    # pass validation by removing/readding pid
    # TODO: add in-database problem schema
    """
    problem.pop("pid", None)
    validate(problem_schema, problem)
    problem["pid"] = pid
    """

    db.problems.update({"pid": pid}, problem)
    api.cache.fast_cache.clear()

    return problem

def search_problems(*conditions):
    """
    Aggregates all problems that contain all of the given properties from the list specified.

    Args:
        conditions: multiple mongo queries to search.
    Returns:
        The list of matching problems.
    """

    db = api.common.get_conn()

    return list(db.problems.find({"$or": list(conditions)}, {"_id":0}))

def insert_problem_from_json(blob):
    """
    Converts json blob of problem(s) into dicts. Runs insert_problem on each one.
    See insert_problem for more information.

    Returns:
        A list of the created problem pids if an array of problems is specified.
    """

    result = json_util.loads(blob)

    if type(result) == list:
        return [insert_problem(problem) for problem in result]
    elif type(result) == dict:
        return insert_problem(result)
    else:
        raise InternalException("JSON blob does not appear to be a list of problems or a single problem.")


def add_problem_dependency(pid1, pid2):
    """
    Adds pid2 to the weightmap of pid1 and updates the threshold

    Args:
      pid1: problem that depends on pid2
      pid2: problem that is a dependency for pid1

    Returns:
      The new weightmap for pid1
    """

    problem1 = get_problem(pid=pid1, show_disabled=True)
    problem2 = get_problem(pid=pid2, show_disabled=True)

    weightmap = problem1['weightmap']
    threshold = problem1['threshold']

    # remove prior dependency if it existed
    threshold -= weightmap.get(problem2['pid'], 0)

    # update dependency
    weightmap[problem2['pid']] = 1
    threshold += 1

    update_problem(pid1, {"weightmap":weightmap, "threshold":threshold})

    return weightmap

def assign_instance_to_team(pid, tid=None):
    """
    Assigns an instance of problem pid to team tid. Updates it in the database.

    Args:
        pid: the problem id
        tid: the team id

    Returns:
        The instance number that was assigned
    """

    team = api.team.get_team(tid=tid)
    problem = get_problem(pid=pid)

    if pid in team["instances"]:
        raise InternalException("Team with tid {} already has an instance of pid {}.".format(tid, pid))

    instance_number = randint(0, len(problem["instances"]) - 1)

    team[pid] = instance_number

    db = api.common.get_conn()
    db.teams.update({"tid": tid}, {"$set": team})

    return instance_number

def get_instance_data(pid, tid):
    """
    Returns the instance dictionary for the specified pid, tid pair

    Args:
        pid: the problem id
        tid: the team id

    Returns:
        The instance dictionary
    """

    instance_map = api.team.get_team(tid=tid)["instances"]
    problem = get_problem(pid=pid, tid=tid)

    if pid not in instance_map:
        iid = assign_instance_to_team(pid, tid)
    else:
        iid = instance_map[pid]

    return problem["instances"][iid]

def get_problem_instance(pid, tid):
    """
    Returns the problem instance dictionary that can be displayed to the user.

    Args:
        pid: the problem id
        tid: the team id

    Returns:
        The problem instance
    """

    problem = deepcopy(get_problem(pid=pid, tid=tid))
    instance = get_instance_data(pid, tid)

    problem.pop("instances")
    problem.update(instance)
    return problem

def grade_problem(pid, key, tid=None):
    """
    Grades the problem with its associated flag.

    Args:
        tid: tid if provided
        pid: problem's pid
        key: user's submission
    Returns:
        A dict.
        correct: boolean
        points: number of points the problem is worth.
        message: message indicating the correctness of the key.
    """

    if tid is None:
        tid = api.user.get_user()["tid"]

    problem = get_problem(pid=pid, tid=tid)
    instance = get_instance_data(pid, tid)

    correct_key = instance['flag']
    correct = correct_key in key # NOTE: is this always correct?

    return {
        "correct": correct,
        "points": problem["score"],
        "message": "That is correct!" if correct else "That is incorrect!"
    }

@log_action
def submit_key(tid, pid, key, uid=None, ip=None):
    """
    User problem submission. Problem submission is inserted into the database.

    Args:
        tid: user's team id
        pid: problem's pid
        key: answer text
        uid: user's uid
    Returns:
        A dict.
        correct: boolean
        points: number of points the problem is worth.
        message: message indicating the correctness of the key.
    """

    db = api.common.get_conn()
    validate(submission_schema, {"tid": tid, "pid": pid, "key": key})

    if pid not in get_unlocked_pids(tid):
        raise InternalException("You can't submit flags to problems you haven't unlocked.")

    if pid in get_solved_pids(tid=tid):
        exp = WebException("You have already solved this problem.")
        exp.data = {'code': 'solved'}
        raise exp

    user = api.user.get_user(uid=uid)
    if user is None:
        raise InternalException("User submitting flag does not exist.")

    uid = user["uid"]

    result = grade_problem(pid, key, tid)

    problem = get_problem(pid=pid)

    eligibility = api.team.get_team(tid=tid)['eligible']

    submission = {
        'uid': uid,
        'tid': tid,
        'timestamp': datetime.utcnow(),
        'pid': pid,
        'ip': ip,
        'key': key,
        'eligible': eligibility,
        'category': problem['category'],
        'correct': result['correct']
    }

    if (key, pid) in [(submission["key"], submission["pid"]) for submission in  get_submissions(tid=tid)]:
        exp = WebException("You or one of your teammates has already tried this solution.")
        exp.data = {'code': 'repeat'}
        raise exp

    db.submissions.insert(submission)

    if submission["correct"]:
        api.cache.invalidate_memoization(api.stats.get_score, {"kwargs.tid":tid}, {"kwargs.uid":uid})
        api.cache.invalidate_memoization(get_unlocked_pids, {"args":tid})
        api.cache.invalidate_memoization(get_solved_pids, {"kwargs.tid":tid}, {"kwargs.uid":uid})

        api.cache.invalidate_memoization(api.stats.get_score_progression, {"kwargs.tid":tid}, {"kwargs.uid":uid})

        api.achievement.process_achievements("submit", {"uid": uid, "tid": tid, "pid": pid})

    return result


def count_submissions(pid=None, uid=None, tid=None, category=None, correctness=None, eligibility=None):
    db = api.common.get_conn()
    match = {}
    if uid is not None:
        match.update({"uid": uid})
    elif tid is not None:
        match.update({"tid": tid})

    if pid is not None:
        match.update({"pid": pid})

    if category is not None:
        match.update({"category": category})

    if correctness is not None:
        match.update({"correct": correctness})

    if eligibility is not None:
        match.update({"eligible": eligibility})

    return db.submissions.find(match, {"_id": 0}).count()


def get_submissions(pid=None, uid=None, tid=None, category=None, correctness=None, eligibility=None):
    """
    Gets the submissions from a team or user.
    Optional filters of pid or category.

    Args:
        uid: the user id
        tid: the team id

        category: category filter.
        pid: problem filter.
        correctness: correct filter
    Returns:
        A list of submissions from the given entity.
    """

    db = api.common.get_conn()

    match = {}

    if uid is not None:
        match.update({"uid": uid})
    elif tid is not None:
        match.update({"tid": tid})

    if pid is not None:
        match.update({"pid": pid})

    if category is not None:
        match.update({"category": category})

    if correctness is not None:
        match.update({"correct": correctness})

    if eligibility is not None:
        match.update({"eligible": eligibility})

    return list(db.submissions.find(match, {"_id":0}))

def clear_all_submissions():
    """
    Removes all submissions from the database.
    """

    db = api.common.get_conn()
    db.submissions.remove()

def clear_submissions(uid=None, tid=None, pid=None):
    """
    Clear submissions for a given team, user, or problems.

    Args:
        uid: the user's uid to clear from.
        tid: the team's tid to clear from.
        pid: the pid to clear from.
    """

    db = api.common.get_conn()

    match = {}


    if pid is not None:
        match.update({"pid", pid})
    elif uid is not None:
        match.update({"uid": uid})
    elif tid is not None:
        match.update({"tid": tid})
    else:
        raise InternalException("You must supply either a tid, uid, or pid")

    return db.submissions.remove(match)

def invalidate_submissions(pid=None, uid=None, tid=None):
    """
    Invalidates the submissions for a given problem. Can be filtered by uid or tid.
    Passing no arguments will invalidate all submissions.

    Args:
        pid: the pid of the problem.
        uid: the user's uid that will his submissions invalidated.
        tid: the team's tid that will have their submissions invalidated.
    """

    db = api.common.get_conn()

    match = {}

    if pid is not None:
        match.update({"pid": pid})

    if uid is not None:
        match.update({"uid": uid})
    elif tid is not None:
        match.update({"tid": tid})

    db.submissions.update(match, {"correct": False})

def reevaluate_submissions_for_problem(pid):
    """
    In the case of the problem being updated, this will reevaluate submissions for a problem.

    Args:
        pid: the pid of the problem to be reevaluated.
    """

    db = api.common.get_conn()

    get_problem(pid=pid, show_disabled=True)

    keys = {}
    for submission in get_submissions(pid=pid):
        key = submission["key"]
        if key not in keys:
            result = grade_problem(pid, key, submission["tid"])
            if result["correct"] != submission["correct"]:
                keys[key] = result["correct"]
            else:
                keys[key] = None

    for key, change in keys.items():
        if change is not None:
            db.submissions.update({"key": key}, {"$set": {"correct": change}}, multi=True)

def reevaluate_all_submissions():
    """
    In the case of the problem being updated, this will reevaluate all submissions.
    """

    api.cache.clear_all()
    for problem in get_all_problems(show_disabled=True):
        reevaluate_submissions_for_problem(problem["pid"])

@api.cache.memoize(timeout=60, fast=True)
def get_problem(pid=None, name=None, tid=None, show_disabled=False):
    """
    Gets a single problem.

    Args:
        pid: The problem id
        name: The name of the problem
        show_disabled: Boolean indicating whether or not to show disabled problems.
    Returns:
        The problem dictionary from the database
    """

    db = api.common.get_conn()

    match = {}

    if pid is not None:
        match.update({'pid': pid})
    elif name is not None:
        match.update({'name': name})
    else:
        raise InternalException("Must supply pid or display name")

    if tid is not None and pid not in get_unlocked_pids(tid):
        raise InternalException("You cannot get this problem")

    if not show_disabled:
        match.update({"disabled": False})

    db = api.common.get_conn()
    problem = db.problems.find_one(match, {"_id":0})

    if problem is None:
        raise SevereInternalException("Could not find problem! You gave " + str(match))

    return problem

def get_all_problems(category=None, show_disabled=False):
    """
    Gets all of the problems in the database.

    Args:
        category: Optional parameter to restrict which problems are returned
        show_disabled: Boolean indicating whether or not to show disabled problems.
    Returns:
        List of problems from the database
    """

    db = api.common.get_conn()

    match = {}
    if category is not None:
        match.update({'category': category})

    if not show_disabled:
        match.update({'disabled': False})

    return list(db.problems.find(match, {"_id":0}).sort('score', pymongo.ASCENDING))

@api.cache.memoize()
def get_solved_pids(tid=None, uid=None, category=None):
    """
    Gets the solved pids for a given team or user.

    Args:
        tid: The team id
        category: Optional parameter to restrict which problems are returned
    Returns:
        List of solved problem ids
    """

    return list(set([sub['pid'] for sub in get_submissions(tid=tid, uid=uid, category=category, correctness=True)]))

def get_solved_problems(tid=None, uid=None, category=None):
    """
    Gets the solved problems for a given team or user.

    Args:
        tid: The team id
        category: Optional parameter to restrict which problems are returned
    Returns:
        List of solved problem dictionaries
    """

    return [get_problem(pid=pid) for pid in get_solved_pids(tid=tid, uid=uid, category=category)]

@api.cache.memoize()
def get_unlocked_pids(tid, category=None):
    """
    Gets the unlocked pids for a given team.

    Args:
        tid: The team id
        category: Optional parameter to restrict which problems are returned
    Returns:
        List of unlocked problem ids
    """

    solved = get_solved_problems(tid=tid, category=category)
    team = api.team.get_team(tid=tid)

    unlocked = []
    for problem in get_all_problems():
        if 'weightmap' not in problem or 'threshold' not in problem:
            unlocked.append(problem['pid'])
        else:
            weightsum = sum(problem['weightmap'].get(p['pid'], 0) for p in solved)
            if weightsum >= problem['threshold']:
                unlocked.append(problem['pid'])

    for pid in unlocked:
        if pid not in team["instances"]:
            assign_instance_to_team(pid, tid)

    return unlocked

def get_unlocked_problems(tid, category=None):
    """
    Gets the unlocked problems for a given team.

    Args:
        tid: The team id
        category: Optional parameter to restrict which problems are returned
    Returns:
        List of unlocked problem dictionaries
    """

    solved = get_solved_pids(tid=tid)
    unlocked = [get_problem_instance(pid, tid) for pid in get_unlocked_pids(tid, category=category)]
    for problem in unlocked:
        problem["solved"] = problem["pid"] in solved
    return unlocked
