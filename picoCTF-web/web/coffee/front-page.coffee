Input = ReactBootstrap.Input
Row = ReactBootstrap.Row
Col = ReactBootstrap.Col
Button = ReactBootstrap.Button
Panel = ReactBootstrap.Panel
Glyphicon = ReactBootstrap.Glyphicon
ButtonInput = ReactBootstrap.ButtonInput
ButtonGroup = ReactBootstrap.ButtonGroup
Alert = ReactBootstrap.Alert

update = React.addons.update

LoginForm = React.createClass

  render: ->
    userGlyph = <Glyphicon glyph="user"/>
    lockGlyph = <Glyphicon glyph="lock"/>

    formButton = if @props.status == "Login" then \

    q = "'" #My syntax highlighting can't handle literal quotes in jsx. :(
    if @props.status == "Reset"
      <Panel>
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
      showEmailFilter = (->
        <Alert bsStyle="warning">
          You can register provided you have an email for one of these domains: <strong>{@props.emailFilter.join ", "}</strong>.
        </Alert>
      ).bind this

      registrationForm = if @props.status == "Register" then \
        <span>
          <Row>
            {if @props.emailFilter.length > 0 then showEmailFilter() else <span/>}
            <Col md={6}>
              <Input type="text" id="first-name" valueLink={@props.firstname} label="First Name"/>
            </Col>
            <Col md={6}>
              <Input type="text" id="last-name" valueLink={@props.lastname} label="Last Name"/>
            </Col>
          </Row>
          <Row>
            <Col md={12}>
              <Input type="email" id="email" valueLink={@props.email} label="E-mail"/>
            </Col>
          </Row>
          <ButtonInput type="submit">Register</ButtonInput>
        </span> else <span/>

      <Panel>
        <form key={@props.status} onSubmit={if @props.status == "Login" then @props.onLogin else @props.onRegistration}>
          <Input type="text" id="username" valueLink={@props.username} addonBefore={userGlyph} label="Username"/>
          <Input type="password" id="password" valueLink={@props.password} addonBefore={lockGlyph} label="Password"/>
          <Row>
            <Col md={6}>
              {if @props.status == "Register" then \
                <span className="pad">Go back to <a onClick={@props.setPage.bind null, "Login"}>Login</a>.</span>
              else <span>
                <Button type="submit">Login</Button>
                <Button id="set-register" onClick={@props.setPage.bind null, "Register"}>Register</Button>
              </span>}
            </Col>
            <Col md={6}>
              <a className="pad" onClick={@props.setPage.bind null, "Reset"}>Need to reset your password?</a>
            </Col>
          </Row>
          {registrationForm}
        </form>
      </Panel>


TeamManagementForm = React.createClass
  mixins: [React.addons.LinkedStateMixin]

  getInitialState: ->
    {}

  onTeamRegistration: (e) ->
    e.preventDefault()
    apiCall "POST", "/api/team/create", {team_name: @state.team_name, team_password: @state.team_password}
    .done (resp) ->
      switch resp.status
        when 0
            apiNotify resp
        when 1
            document.location.href = "/profile"

  onTeamJoin: (e) ->
    e.preventDefault()
    apiCall "POST", "/api/team/join", {team_name: @state.team_name, team_password: @state.team_password}
    .done (resp) ->
      switch resp.status
        when 0
            apiNotify resp
        when 1
            document.location.href = "/profile"

  render: ->

    towerGlyph = <Glyphicon glyph="tower"/>
    lockGlyph = <Glyphicon glyph="lock"/>

    <Panel>
      <form onSubmit={@onTeamJoin}>
        <Input type="text" valueLink={@linkState "team_name"} addonBefore={towerGlyph} label="Team Name" required/>
        <Input type="password" valueLink={@linkState "team_password"} addonBefore={lockGlyph} label="Team Password" required/>
        <Col md={6}>
          <span> <Button type="submit">Join Team</Button>
            <Button onClick={@onTeamRegistration}>Register Team</Button>
          </span>
        </Col>
        <Col md={6}>
          <a href="#" onClick={() -> document.location.href = "/profile"}>Play as an individual.</a>
        </Col>
      </form>
    </Panel>

AuthPanel = React.createClass
  mixins: [React.addons.LinkedStateMixin]
  getInitialState: ->
    page: "Login"
    settings: {}

  componentWillMount: ->
    apiCall "GET", "/api/team/settings"
    .done ((req) ->
      @setState update @state,
        settings: $set: req.data
     ).bind this

  onRegistration: (e) ->
    e.preventDefault()
    apiCall "POST", "/api/user/create_simple", @state
    .done ((resp) ->
      apiNotify resp
      switch resp.status
        when 1
          if @state.settings.max_team_size > 1
            @setPage "Team Management"
          else
            document.location.href = "/profile"
    ).bind this

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

    if @state.page == "Team Management"
      <div>
        <Col md={6} mdOffset={3}>
          <TeamManagementForm/>
        </Col>
      </div>
    else
      <div>
        <Col md={6} mdOffset={3}>
          <LoginForm setPage={@setPage} status={@state.page} onRegistration={@onRegistration}
            onLogin={@onLogin} onPasswordReset={@onPasswordReset} emailFilter={@state.settings.email_filter}
            {...links}/>
        </Col>
      </div>

$ ->
  React.render <AuthPanel/>, document.getElementById("auth-box")
