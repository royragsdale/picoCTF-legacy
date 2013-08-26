window.load_problems = ->
  $.ajax(type: "GET", cache: false, url: "/api/problems", dataType: "json")
    .done (data) ->
      html = '<div class="contentbox row-fluid">'
      for d in data
        id = d['pid']
        html += """
                <div class="row-fluid">
                <div class="offset1 span10">
                <div class="basic_view_header">
                <h3>#{d['displayname']}: #{d['basescore']}
        #{if d['correct'] then '<span class="solved">Solved</span>' else '<span class="unsolved">Unsolved</span>'}
                </h3>
                </div>
                <div class="basic_view_body">
        #{d['desc']}
                <div id=msg_#{id}></div>
                <form onsubmit="handle_submit('#{id}'); return false;" class="form-inline" id="form_#{id}">
                <input id="#{id}" type="text" autocomplete="off"/>
                <button class="btn" type="submit">Submit!</button>
                </form>
                </div>
                </div>
                </div>"""
      html += '</div>'
      $("#problems_holder").html html
      $(".basic_view_header").click ->
        $(this).next().toggle('fast')
      $(".solved").parent().parent().next().hide()