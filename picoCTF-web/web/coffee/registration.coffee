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

  apiCall "POST", "/api/user/create_simple", registrationData
  .done (data) ->
    switch data['status']
      when 0
        $("#register-button-create").apiNotify(data, {position: "right"})
        ga('send', 'event', 'Registration', 'Failure', "NewTeam::" + data.message)
        reloadCaptcha()
      when 1
            document.location.href = "/profile"

$ ->
  apiCall "GET", "/api/user/status", {}
  .done (data) ->
    if data.data.enable_captcha
        Recaptcha.create(data.data.reCAPTCHA_public_key, "captcha", { theme: "red" })

  $("#user-registration-form").on "submit", submitRegistration
