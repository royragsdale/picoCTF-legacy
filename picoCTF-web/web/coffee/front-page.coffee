Input = ReactBootstrap.Input
Row = ReactBootstrap.Row
Col = ReactBootstrap.Col
Button = ReactBootstrap.Button
Panel = ReactBootstrap.Panel
Glyphicon = ReactBootstrap.Glyphicon
ButtonInput = ReactBootstrap.ButtonInput

update = React.addons.update

LoginForm = React.createClass
  render: ->
    userGlyph = <Glyphicon glyph="user"/>
    lockGlyph = <Glyphicon glyph="lock"/>

    formButton = if @props.status == "Login" then \

    q = "'" #My syntax highlighting can't handle literal quotes in jsx. :(
    if @props.status == "Reset"
      <Panel className="form-test">
        <form onSubmit={@props.onPasswordReset}>
          <p><i>A password reset link will be sent the user{q}s email.</i></p>
          <Input type="text" valueLink={@props.username} addonBefore={userGlyph} placeholder="Username" required="visible"/>
          <div style={{height: "70px"}}/>
          <Row>
            <Col md={6}>
              <ButtonInput type="submit">Reset Password</ButtonInput>
            </Col>
            <Col md={6}>
              <span className="pull-right pad">Go back to <a onClick={@props.setPage.bind null, "Login"}>Login</a>.</span>
            </Col>
          </Row>
        </form>
      </Panel>
    else
      <Panel className="form-test">
        <form onSubmit={@props.onLogin}>
          <Input type="text" valueLink={@props.username} addonBefore={userGlyph} label="Username"/>
          <Input type="password" valueLink={@props.password} addonBefore={lockGlyph} label="Password"/>
          <Row>
            <Col md={6}>
              {if @props.status == "Register" then \
                <span className="pad">Go back to <a onClick={@props.setPage.bind null, "Login"}>Login</a>.</span>
              else <ButtonInput type="submit">Login</ButtonInput>}
            </Col>
            <Col md={6}>
              <a className="pad" onClick={@props.setPage.bind null, "Reset"}>Need to reset your password?</a>
            </Col>
          </Row>
        </form>
      </Panel>

RegistrationForm = React.createClass
  render: ->
    if @props.status == "Login" or @props.status == "Reset"
      <Panel className="form-test">
        <h3>Welcome to CyberStakes Live!</h3>
        <h4>Please Login or <a onClick={@props.setPage.bind null, "Register"}>Register</a>.</h4>
      </Panel>
    else if @props.status == "Register"
      <Panel className="form-test">
        <form onSubmit={@props.onRegistration}>
          <Row>
            <Col md={6}>
              <Input type="text" valueLink={@props.firstname} label="Firstname"/>
            </Col>
            <Col md={6}>
              <Input type="text" valueLink={@props.lastname} label="Lastname"/>
            </Col>
          </Row>
          <Row>
            <Col md={12}>
              <Input type="text" valueLink={@props.email} label="E-Mail"/>
            </Col>
          </Row>
          <ButtonInput type="submit" onClick={@props.onRegistration}>Register</ButtonInput>
        </form>
      </Panel>

AuthPanel = React.createClass
  mixins: [React.addons.LinkedStateMixin]
  getInitialState: ->
    page: "Login"

  onRegistration: (e) ->
    e.preventDefault()
    apiCall "POST", "/api/user/create_simple", @state
    .done (resp) ->
      switch resp.status
        when 0
          apiNotify resp
        when 1
          document.location.href = "/profile"

  onPasswordReset: (e) ->
    e.preventDefault()
    apiCall "POST", "/api/user/reset_password", {username: @state.username}
    .done ((resp) ->
      apiNotify resp
      if resp.status == 1
        @setPage "Login"
    ).bind this

  onLogin: (e) ->
    e.preventDefault()
    apiCall "POST", "/api/user/login", {username: @state.username, password: @state.password}
    .done (resp) ->
      switch resp.status
        when 0
            apiNotify resp
        when 1
            if resp.data.teacher
              document.location.href = "/classroom"
            else
              document.location.href = "/profile"

  setPage: (page) ->
    @setState update @state,
        page: $set: page

  componentDidMount: ->
    $("input").prop 'required', true

  componentDidUpdate: ->
    $("input").prop 'required', true

  render: ->
    links =
    username: @linkState "username"
    password: @linkState "password"
    lastname: @linkState "lastname"
    firstname: @linkState "firstname"
    email: @linkState "email"

    <div>
      <Col md={6}>
        <LoginForm setPage={@setPage} status={@state.page}
          onLogin={@onLogin} onPasswordReset={@onPasswordReset} {...links}/>
      </Col>
      <Col md={6}>
        <RegistrationForm setPage={@setPage} status={@state.page}
          onRegistration={@onRegistration} {...links}/>
      </Col>
    </div>

$ ->
  React.render <AuthPanel/>, document.getElementById("auth-box")
