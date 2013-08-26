window.load_scoreboards = ->
  console.log "loading scoreboards..."
  $.ajax(type: "GET", cache: false, url: "/api/scoreboards", dataType: "json")
  .done (data) ->
    html_select = '';
    html_scores = '';
    for d in data
      if d['path']?
        group = d.group
        $.ajax(type: "GET", url: d['path'], dataType: "html", cache: false, async: true)
        .done (stat) ->
          if group == 'Public'
            $('#public_scoreboard_container').html stat
          else
            html_select += """<li><a onclick="switch_scoreboard('#{group}');">#{group}</a></li>"""
            html_scores += """<div style='display: none;' id='scoreboard_#{group}' class='scoreboard'>#{stat}</div>"""
      else
        html_select += """<li><a onclick="switch_scoreboard('#{d.group}');">#{d.group}</a></li>"""
        html_scores += "<div style='display: none;' id='scoreboard_#{d.group}' class='scoreboard'><table class='table'><tbody><tr><th>Place</th><th>Team</th><th>Affiliation</th><th>Score</th></tr>"
        for s, idx in d['scores']
          html_scores += "<tr><td>#{idx+1}</td><td class='teamname'>#{s['teamname']}</td><td class='affiliation'>#{s['affiliation']}</td><td>#{s['score']}</td></tr>"
        html_scores += "</tbody></table></div>"
    $('#scoreboard_selector').html html_select
    $('#scoreboard_container').html html_scores
    if !!window.location.hash
      !switch_scoreboard(window.location.hash.substr(1))
    else
      $('div.scoreboard').first().slideDown('fast')

window.switch_scoreboard = (group) ->
  if $("#scoreboard_"+group).length > 0
    window.location.hash = "#" + group
    if $("div.scoreboard:visible").length > 0
      $("div.scoreboard:visible").slideUp('fast', -> $("#scoreboard_" + group).slideDown('fast'))
    else
      $("#scoreboard_" + group).slideDown('fast')
  else
    $('div.scoreboard').first().slideDown('fast')
  return false

window.load_solved_problems = ->
  $.ajax(type: "GET", cache: false, url: "/api/problems/solved", dataType: "json")
  .done (data) ->
    html = '<table class=\"table\">'
    if data.length != 0
      html += "<tr><th>Points Awarded</th><th>Solved Problem</th></tr>";
      for d in data
        html += "<tr><td>#{d['basescore']}</td><td>#{d['displayname']}</td></tr>"
      html += "</table>"
      $("#problems_solved").html html
    else
      html += "You haven't solved any problems yet."
      $("#problems_solved").html html

window.load_teamscore = ->
  $.ajax(type: "GET", cache: false, url: "/api/score", dataType: "json")
  .done (data) ->
    $('#team_status').html "<h3>Team Status - #{data['score']}</h3>"