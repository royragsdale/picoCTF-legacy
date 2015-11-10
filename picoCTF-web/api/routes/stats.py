from flask import Flask, request, session, send_from_directory, render_template
from flask import Blueprint
import api
import bson

from api.common import WebSuccess, WebError
from api.annotations import api_wrapper, require_login, require_teacher, require_admin, check_csrf
from api.annotations import block_before_competition, block_after_competition
from api.annotations import log_action

blueprint = Blueprint("stats_api", __name__)

@blueprint.route('/team/solved_problems', methods=['GET'])
@api_wrapper
@require_login
@block_before_competition(WebError("The competition has not begun yet!"))
def get_team_solved_problems_hook():
    tid = request.args.get("tid", None)
    stats = {
        "problems": api.stats.get_problems_by_category(),
        "members": api.stats.get_team_member_stats(tid)
    }

    return WebSuccess(data=stats)

@blueprint.route('/team/score_progression', methods=['GET'])
@api_wrapper
@require_login
@block_before_competition(WebError("The competition has not begun yet!"))
def get_team_score_progression():
    category = request.args.get("category", None)

    tid = api.user.get_team()["tid"]

    return WebSuccess(data=api.stats.get_score_progression(tid=tid, category=category))

@blueprint.route('/scoreboard', methods=['GET'])
@api_wrapper
@block_before_competition(WebError("The competition has not begun yet!"))
def get_scoreboard_hook():
    result = {}
    result['public'] = api.stats.get_all_team_scores(eligible=True)
    result['groups'] = []

    if api.auth.is_logged_in():
        user = api.user.get_user()
        if not api.team.get_team(tid=user["tid"])["eligible"]:
            result['ineligible'] = api.stats.get_all_team_scores(eligible=False)
        for group in api.team.get_groups(uid=user["uid"]):
            result['groups'].append({
                'gid': group['gid'],
                'name': group['name'],
                'scoreboard': api.stats.get_group_scores(gid=group['gid'])
            })

    return WebSuccess(data=result)

@blueprint.route('/top_teams/score_progression', methods=['GET'])
@api_wrapper
def get_top_teams_score_progressions_hook():
    eligible = request.args.get("eligible", "true")

    eligible = bson.json_util.loads(eligible)

    return WebSuccess(data=api.stats.get_top_teams_score_progressions(eligible=eligible))

@blueprint.route('/group/score_progression', methods=['GET'])
@api_wrapper
def get_group_top_teams_score_progressions_hook():
    gid = request.args.get("gid", None)
    return WebSuccess(data=api.stats.get_top_teams_score_progressions(gid=gid, eligible=True))
