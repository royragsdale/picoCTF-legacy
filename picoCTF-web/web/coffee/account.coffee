updatePassword = (e) ->
  e.preventDefault()
  apiCall "POST", "/api/user/update_password", $("#password-update-form").serializeObject()
  .done (data) ->
    switch data['status']
      when 1
        ga('send', 'event', 'Authentication', 'UpdatePassword', 'Success')
      when 0
        ga('send', 'event', 'Authentication', 'UpdatePassword', 'Failure::' + data.message)
    apiNotify data, "/account"

resetPassword = (e) ->
  e.preventDefault()
  form = $("#password-reset-form").serializeObject()
  form["reset-token"] = window.location.hash.substring(1)
  apiCall "POST", "/api/user/confirm_password_reset", form
  .done (data) ->
    ga('send', 'event', 'Authentication', 'ResetPassword', 'Success')
    apiNotify data, "/"

disableAccount = (e) ->
  e.preventDefault()
  confirmDialog("This will disable your account, drop you from your team, and prevent you from playing!", "Disable Account Confirmation", "Disable Account", "Cancel",
  () ->
    form = $("#disable-account-form").serializeObject()
    apiCall "POST", "/api/user/disable_account", form
    .done (data) ->
      ga('send', 'event', 'Authentication', 'DisableAccount', 'Success')
      apiNotify data, "/")

Input = ReactBootstrap.Input
Row = ReactBootstrap.Row
Col = ReactBootstrap.Col
Button = ReactBootstrap.Button
Panel = ReactBootstrap.Panel
Glyphicon = ReactBootstrap.Glyphicon
ButtonInput = ReactBootstrap.ButtonInput
ButtonGroup = ReactBootstrap.ButtonGroup

update = React.addons.update

# Should figure out how we want to share components.
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

    console.log @linkState, "asd"
    t = @linkState "team_name"
    console.log @state, t
    towerGlyph = <Glyphicon glyph="tower"/>
    lockGlyph = <Glyphicon glyph="lock"/>

    <Panel header="Team Management">
      <form onSubmit={@onTeamJoin}>
        <Input type="text" valueLink={@linkState "team_name"} addonBefore={towerGlyph} label="Team Name" required/>
        <Input type="password" valueLink={@linkState "team_password"} addonBefore={lockGlyph} label="Team Password" required/>
        <Col md={6}>
          <span> <Button type="submit">Join Team</Button>
            <Button onClick={@onTeamRegistration}>Register Team</Button>
          </span>
        </Col>
      </form>
    </Panel>

$ ->
  $("#password-update-form").on "submit", updatePassword
  $("#password-reset-form").on "submit", resetPassword
  $("#disable-account-form").on "submit", disableAccount

  React.render <TeamManagementForm/>, document.getElementById("team-management")
