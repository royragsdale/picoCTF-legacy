recaptchaPublicKey = ""

reloadCaptcha = ->
  apiCall "GET", "/api/user/status", {}
  .done (data) ->
    if data.data.enable_captcha
        Recaptcha.reload()
    ga('send', 'event', 'Registration', 'NewCaptcha')


setRequired = ->
    $('#user-registration-form :input').each () ->
        if not $(this).is(':checkbox')
            if not $(this).is(':radio')
                $(this).prop('required', $(this).is(":visible"))


submitRegistration = (e) ->
  e.preventDefault()
  registrationData = $("#user-registration-form").serializeObject()

  # set defaults for cyberstakes online
  registrationData['country'] = 'US'
  registrationData['create-new-team'] = true
  registrationData['team-name-new'] = registrationData['username']
  registrationData['team-password-new'] = "hack"

  apiCall "POST", "/api/user/create", registrationData
  .done (data) ->
    switch data['status']
      when 0
        $(submitButton).apiNotify(data, {position: "right"})
        ga('send', 'event', 'Registration', 'Failure', "NewTeam::" + data.message)
        reloadCaptcha()
      when 1
            document.location.href = "/profile"

$ ->
  apiCall "GET", "/api/user/status", {}
  .done (data) ->
    if data.data.enable_captcha
        Recaptcha.create(recaptchaPublicKey, "captcha", { theme: "red" })

  $("#user-registration-form").on "submit", submitRegistration
