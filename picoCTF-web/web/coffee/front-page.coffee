Input = ReactBootstrap.Input
Row = ReactBootstrap.Row
Col = ReactBootstrap.Col
Button = ReactBootstrap.Button
Panel = ReactBootstrap.Panel
Glyphicon = ReactBootstrap.Glyphicon

update = React.addons.update

LoginForm = React.createClass
  render: ->
    userGlyph = <Glyphicon glyph="user"/>
    lockGlyph = <Glyphicon glyph="lock"/>

    formButton = if @props.status == "Login" then \
    <div>
      <Button>Login</Button> <a className="pull-right pad">Need to reset your password?</a>
    </div> else \
    <span className="pad">Go back to <a onClick={@props.setPage.bind null, "Login"}>Login</a>.</span>

    <Panel className="form-test">
      <Input type="text" valueLink={@props.username} addonBefore={userGlyph} label="Username"/>
      <Input type="text" valueLink={@props.password} addonBefore={lockGlyph} label="Password"/>
      <div>
        {formButton}
      </div>
    </Panel>

RegistrationForm = React.createClass
  render: ->
    if @props.status == "Login"
      <Panel className="form-test">
        <h3>Welcome to CyberStakes Live!</h3>
        <h4>Please Login or <a onClick={@props.setPage.bind null, "Register"}>Register</a>.</h4>
      </Panel>
    else if @props.status == "Register"
      <Panel className="form-test">
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
        <Button onClick={@props.onRegister}>Register</Button>
      </Panel>

AuthPanel = React.createClass
  mixins: [React.addons.LinkedStateMixin]
  getInitialState: ->
    page: "Login"

  setPage: (page) ->
    @setState update @state,
        page: $set: page

  render: ->
    links =
    username: @linkState "username"
    password: @linkState "password"
    lastname: @linkState "lastname"
    firstname: @linkState "firstname"
    email: @linkState "email"

    <div>
      <Col md={6}>
        <LoginForm setPage={@setPage} status={@state.page} {...links}/>
      </Col>
      <Col md={6}>
        <RegistrationForm setPage={@setPage} status={@state.page} {...links}/>
      </Col>
    </div>

$ ->
  React.render <AuthPanel/>, document.getElementById("auth-box")
