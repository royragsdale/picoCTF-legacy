#!/usr/bin/python3

import api

"""
teams = api.teams.filter(score > 0)
for server in api.shell_servers.get_online_servers():
  shell = server.get_ssh()
  for team in teams:
    current_head = db.submission_heads.find(tid)
    most_recent_sub = db.submissions.get_most_recent(tid)

    if current_head is None or current_head < most_recent_sub:
      unlocked_problems = api.problems.get_unlocked(team)

      for user in team.get_enabled_users():
        user_sym_links = shell.get_sym_links(user)
        additional_sym_links = unlocked_problems / user_sym_links
        removable_sym_links = user_sym_links / unlocked_problems

        shell.sym_links.add(user, additional_sym_links)
        shell.sym_links.remove(user, removable_sym_links)
"""

def run():
    db = api.common.get_conn()

    teams = api.team.get_all_teams(show_ineligible=True)

    for server in api.shell_servers.get_servers():
        shell = api.shell_servers.get_connection(server["sid"])

        submission_heads = db.submission_heads.find_one({"sid": server["sid"]})
        if submission_heads is None:
            db.submission_heads.insert({"sid": server["sid"], "heads": {}})
            submission_heads = db.submission_heads.find_one({"sid": server["sid"]})

        submission_heads = submission_heads["heads"]
        for team in teams:
            submission = api.problem.get_most_recent_submission(tid=team["tid"], correctness=True)
            team_head_pid = submission_heads.get(team["tid"], None)
            if submission is not None and (team_head_pid is None or submission["pid"] != team_head_pid):
                print("Team '%s' is outdated. %s -> %s" % (team["team_name"], team_head_pid, submission["pid"]))

                unlocked_problems = api.problem.get_unlocked_problems(tid=team["tid"])

                db.submission_heads.update({"sid": server["sid"]}, {"$set": {"heads."+team["tid"]: submission["pid"]}})
            else:
                print("Team '%s' up-to-date." % team["team_name"])


