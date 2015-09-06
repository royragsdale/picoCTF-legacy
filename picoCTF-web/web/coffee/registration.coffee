reloadCaptcha = ->
  apiCall "GET", "/api/user/status", {}
  .done (data) ->
    if data.data.enable_captcha
        grecaptcha.reset()
    ga('send', 'event', 'Registration', 'NewCaptcha')


setRequired = ->
    $('#user-registration-form :input').each () ->
        if not $(this).is(':checkbox')
            if not $(this).is(':radio')
                $(this).prop('required', $(this).is(":visible"))


submitRegistration = (e) ->
  e.preventDefault()
  registrationData = $("#user-registration-form").serializeObject()

  apiCall "POST", "/api/user/create_simple", registrationData
  .done (data) ->
    switch data['status']
      when 0
        $(submitButton).apiNotify(data, {position: "right"})
        ga('send', 'event', 'Registration', 'Failure', logType + "::" + data.message)
        grecaptcha.reset()
      when 1
            document.location.href = "/profile"

$ ->
  apiCall "GET", "/api/user/status", {}
  .done (data) ->
    if data.data.enable_captcha
      grecaptcha.render("captcha", { "sitekey": data.data.recaptchaPublicKey })

  $("#user-registration-form").on "submit", submitRegistration
