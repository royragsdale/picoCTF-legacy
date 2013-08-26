window.handle_login = ->
  $.ajax(type: "POST", cache: false, url: "/api/login", dataType: "json", data: {'teamname': $("#reg-team").val(), 'password': $("#reg-pass").val()})
  .done (data) ->
    if data['success'] == 0 || data['success'] == 2
      if typeof(Storage) != "undefined"
        sessionStorage.signInStatus = "notLoggedIn"
      if data['success'] == 0 then alert_class = 'alert-error' else if data['success'] == 2 then alert_class = 'alert-info'
      $('#login_msg').hide().html("<div class=\"alert #{alert_class}\"> #{data['message']} </div>").slideDown('normal')
      setTimeout( ->
        $('#login_msg').slideUp('normal', ->
          $('#login_msg').html('').show())
      , 2000)
    else if data['success'] == 1
      if (typeof(Storage) != "undefined")
        sessionStorage.signInStatus = "loggedIn";
      document.location.href = "compete";

window.handle_forgot_password_submit = ->
  $.ajax(type: "POST", cache: false, url: "/api/requestpasswordreset", dataType: "json", data: {'teamname': $("#reg-team").val()})
  .done (data) ->
    login_msg = $('#login_msg')
    if data['success'] == 0 then alert_class = "alert-error" else if data['success'] == 1 then alert_class = "alert-success"
    login_msg.hide().html("<div class=\"alert #{alert_class}\"> #{data["message"]} </div>").slideDown('normal')
    setTimeout( ->
      login_msg.slideUp('normal', ->
        login_msg.html('').show())
    , 3000)