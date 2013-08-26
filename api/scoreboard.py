__author__ = "Collin Petty"
__copyright__ = "Carnegie Mellon University"
__license__ = "MIT"
__maintainer__ = ["Collin Petty", "Peter Chapman"]
__credits__ = ["David Brumely", "Collin Petty", "Peter Chapman", "Tyler Nighswander", "Garrett Barboza"]
__email__ = ["collin@cmu.edu", "peter@cmu.edu"]
__status__ = "Production"


from datetime import datetime
import json
import group
from common import db
from common import cache
from common import esc

end = datetime(2020, 5, 7, 3, 59, 59)


def get_group_scoreboards(tid):
    """Gets the group scoreboards.

    Because of the multithreaded implementation we rebuild the scoreboard in the aggregator, this call can only
    return a value from cache. This prevents multiple page requests from invoking a scoreboard rebuild simultaneously.
    Get all groups a users is a member of and look for group scoreboards for each of these groups.
    """
    group_scoreboards = []
    groups = group.get_group_membership(tid)
    for g in groups:
        board = cache.get('groupscoreboard_'+g['name'])
        if board is not None:
            group_scoreboards.append(json.loads(board))
    return group_scoreboards


def get_public_scoreboard():
    """Gets the archived public scoreboard.

    Kind of a hack, tells the front end to look for a static page scoreboard rather than sending a 2000+ length
    array that the front end must parse.
    """
    return {'path': '/staticscoreboard.html', 'group': 'Public'}


def load_team_score(tid):
    """Get the score for a team.

    Looks for a cached team score, if not found we query all correct submissions by the team and add up their
    basescores if they exist. Cache the result.
    """
    score = cache.get('teamscore_' + tid)
    if score is not None:
        return score
    s = {d['pid'] for d in list(db.submissions.find({"tid": tid, "correct": True}))}  # ,#"timestamp": {"$lt": end}}))}
    score = sum([d['basescore'] if 'basescore' in d else 0 for d in list(db.problems.find({
        'pid': {"$in": list(s)}}))])
    cache.set('teamscore_' + tid, score, 60 * 60)
    return score


def load_group_scoreboard(group):
    """Build the scoreboard for an entire group of teams.

    Get all of he team names, tid's, and affiliations for all teams that  are a member of the given group.
    Iterate over all of the teams grabbing the last correct submission date (tie breaker). If the last subdate does
    not exist in the cache rebuild it by grabbing all of a teams correct submission and sorting by submission
    timestamp.
    Sort all team score's by their last submission date, we then sort the list by the score. The python sorting
    algorithm is guaranteed stable so equal scores will be ordered by last submission date.
    Cache the entire scoreboard.
    """
    teams = [
        {'tid': t['tid'],
         'teamname': t['teamname'],
         'affiliation': t['affiliation'] if 'affiliation' in t else None}
        for t in list(db.teams.find({'tid': {'$in': group['members']}}, {'tid': 1, 'teamname': 1, 'affiliation': 1}))]
    for t in teams:
        lastsubdate = cache.get('lastsubdate_' + t['tid'])
        if lastsubdate is None:
            subs = list(db.submissions.find({'tid': t['tid'],
                                             'correct': True,
                                             'timestamp': {"$lt": end}}))
            if len(subs) == 0:
                lastsubdate = str(datetime(2000, 01, 01))
            else:
                sortedsubs = sorted(subs, key=lambda k: str(k['timestamp']), reverse=True)
                lastsubdate = str(sortedsubs[0]['timestamp'])
            cache.set('lastsubdate_' + t['tid'], lastsubdate, 60 * 30)
        t['lastsubdate'] = lastsubdate

    teams.sort(key=lambda k: k['lastsubdate'])
    top_scores = [x for x in sorted(
        [{'teamname': esc(t['teamname']),
          'affiliation': esc(t['affiliation']),
          'score': load_team_score(t['tid'])}
         for t in teams], key=lambda k: k['score'], reverse=True) if x['score'] > 0]
    cache.set('groupscoreboard_' + str(group['name']), json.dumps({'group': group['name'], 'scores': top_scores}), 60 * 30)
