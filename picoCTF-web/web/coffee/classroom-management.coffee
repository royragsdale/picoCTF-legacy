Input = ReactBootstrap.Input
Row = ReactBootstrap.Row
Col = ReactBootstrap.Col
Button = ReactBootstrap.Button
Panel = ReactBootstrap.Panel
ListGroup = ReactBootstrap.ListGroup
ListGroupItem = ReactBootstrap.ListGroupItem
Glyphicon = ReactBootstrap.Glyphicon

update = React.addons.update

MemberManagementItem = React.createClass
  render: ->
    user = _.first @props.members
    <Row>
      <Col xs={4}>
        <Row>{user.username}</Row>
        <Row>
          <Col xs={6}>{user.firstname}</Col>
          <Col xs={6}>{user.lastname}</Col>
        </Row>
        <Row>{user.email}</Row>
      </Col>
      <Col xs={8}>
        test
      </Col>
    </Row>

MemberManagement = React.createClass
  render: ->
    <div>
      Group User Management
      <ListGroup>
        {@props.memberInformation.map ((member) ->
          <ListGroupItem>
            <MemberManagementItem {...member}/>
          </ListGroupItem>
        ).bind this}
      </ListGroup>
    </div>

ClassroomManagement = React.createClass
  getInitialState: ->
    name: ""
    settings:
      email_filter: []
    member_information: []

  componentWillMount: ->
    @refreshSettings()

  refreshSettings: ->
    apiCall "GET", "/api/group/settings", {gid: @props.gid}
    .done ((resp) ->
      @setState update @state, $merge: resp.data
    ).bind this

    apiCall "GET", "/api/group/member_information", {gid: @props.gid}
    .done ((resp) ->
      @setState update @state, member_information: $set: resp.data
    ).bind this

  pushUpdates: (modifier) ->
    data = @state

    if modifier
      data.settings = modifier data.settings

    apiCall "POST", "/api/group/settings", {gid: @props.gid, settings: JSON.stringify data.settings}
    .done ((resp) ->
      apiNotify resp
      @refreshSettings()
    ).bind this

  render: ->
    <div>
      <Col xs={6}>
        <MemberManagement memberInformation={@state.member_information}/>
      </Col>
      <Col xs={6}>
        <GroupEmailWhitelist emails={@state.settings.email_filter} pushUpdates={@pushUpdates} gid={@props.gid}/>
      </Col>
    </div>

EmailWhitelistItem = React.createClass
  propTypes:
    email: React.PropTypes.string.isRequired
    pushUpdates: React.PropTypes.func.isRequired

  render: ->
    removeEmail = @props.pushUpdates.bind null, ((data) ->
      update data, {email_filter: {$apply: _.partial _.without, _, @props.email}}
    ).bind this

    <ListGroupItem>
      *@{@props.email}
      <span className="pull-right"><Glyphicon glyph="remove" onClick={removeEmail}/></span>
    </ListGroupItem>

GroupEmailWhitelist = React.createClass
  mixins: [React.addons.LinkedStateMixin]

  getInitialState: -> {}

  propTypes:
    pushUpdates: React.PropTypes.func.isRequired
    emails: React.PropTypes.array.isRequired
    gid: React.PropTypes.string.isRequired

  addEmailDomain: (e) ->
    # It would probably make more sense to this kind of validation server side.
    # However, it can't cause any real issue being here.

    e.preventDefault()

    if _.indexOf(@props.emails, @state.emailDomain) != -1
      apiNotify {status: 0, message: "This email domain has already been whitelisted."}
    else if _.indexOf(@state.emailDomain, "@") != -1
      apiNotify {status: 0, message: "You should not include '@'. I want the email domain that follows '@'."}
    else if _.indexOf(@state.emailDomain, ".") == -1
        apiNotify {status: 0, message: "Your email domain did not include a '.' as I expected. Please make sure this is an email domain."}
    else
      @props.pushUpdates ((data) ->
        update data, {email_filter: {$push: [@state.emailDomain]}}
      ).bind this

  createItemDisplay: ->
    <ListGroup>
      {@props.emails.map ((email, i) ->
        <EmailWhitelistItem key={i} email={email} pushUpdates={@props.pushUpdates}/>
      ).bind this}
    </ListGroup>

  render: ->
    emptyItemDisplay =
      <p>The whitelist is current empty. All emails will be accepted during registration.</p>

    <div>
      <h4>Email Domain Whitelist</h4>
      <form onSubmit={@addEmailDomain}>
        <Row>
          <Input type="text" addonBefore="@ Domain" valueLink={@linkState "emailDomain"}/>
        </Row>
        <Row>
          {if @props.emails.length > 0 then @createItemDisplay() else emptyItemDisplay}
        </Row>
      </form>
    </div>

$ ->
  React.render <ClassroomManagement gid="9fd32927fda84b90a8c1fb7cbb59508f"/>, document.getElementById("group-management")
