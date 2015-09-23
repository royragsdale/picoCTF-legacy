Input = ReactBootstrap.Input
Row = ReactBootstrap.Row
Col = ReactBootstrap.Col
Button = ReactBootstrap.Button
ButtonGroup = ReactBootstrap.ButtonGroup
Panel = ReactBootstrap.Panel
ListGroup = ReactBootstrap.ListGroup
ListGroupItem = ReactBootstrap.ListGroupItem
Glyphicon = ReactBootstrap.Glyphicon
TabbedArea = ReactBootstrap.TabbedArea
TabPane = ReactBootstrap.TabPane

update = React.addons.update

MemberManagementItem = React.createClass
  removeTeam: ->
    apiCall "POST", "/api/group/teacher/leave", {gid: @props.gid, tid: @props.tid}
    .done ((resp) ->
      apiNotify resp
      @props.refresh()
    ).bind this

  switchUserRole: (uid) ->
    console.log uid, "?"
    apiCall "POST", "/api/group/teacher/role_switch", {gid: @props.gid, uid: uid, role: "teacher"}
    .done ((resp) ->
      apiNotify resp
      @props.refresh()
    ).bind this

  render: ->
    user = _.first @props.members
    console.log user
    <ListGroupItem>
      <Row>
        <Col xs={2}>
          <Button bsStyle="primary" className="btn-sq">
            <Glyphicon glyph="user" bsSize="large"/>
            <p className="text-center">{if @props.teacher then "Teacher" else "User"}</p>
          </Button>
        </Col>
        <Col xs={6}>
          <h4>{user.username}</h4>
          <p>
            <strong>Name:</strong> {user.firstname} {user.lastname}
          </p>
          <p><strong>Email:</strong> {user.email}</p>
        </Col>
        <Col xs={4}>
          <ButtonGroup vertical>
            <Button onClick={@removeTeam}>Remove User</Button>
            <Button onClick={@switchUserRole.bind(null, user.uid)}>Make Teacher</Button>
          </ButtonGroup>
        </Col>
      </Row>
    </ListGroupItem>

MemberInvitePanel = React.createClass
  mixins: [React.addons.LinkedStateMixin]

  propTypes:
    gid: React.PropTypes.string.isRequired

  getInitialState: ->
    role: "member"

  inviteUser: (e) ->
    e.preventDefault()
    apiCall "POST", "/api/group/invite", {gid: @props.gid, email: @state.email, role: @state.role}
    .done ((resp) ->
      apiNotify resp
      @setState update @state, $set: email: ""
      @props.refresh()
    ).bind this

  render: ->
    <Panel>
      <form onSubmit={@inviteUser}>
        <Col xs={8}>
          <Input type="email" label="E-mail" valueLink={@linkState "email"}/>
        </Col>
        <Col xs={4}>
          <Input type="select" label="Role" placeholder="Member" valueLink={@linkState "role"}>
            <option value="member">Member</option>
            <option value="teacher">Teacher</option>
          </Input>
        </Col>
        <Col xs={4}>
          <Button onClick={@inviteUser}>Invite User</Button>
        </Col>
      </form>
    </Panel>

MemberManagement = React.createClass
  render: ->
    <div>
      <h4>User Management</h4>
      <MemberInvitePanel gid={@props.gid} refresh={@props.refresh}/>
      <ListGroup>
        {@props.memberInformation.map ((member, i) ->
          <MemberManagementItem key={i} gid={@props.gid} refresh={@props.refresh} {...member}/>
        ).bind this}
      </ListGroup>
    </div>

GroupManagement = React.createClass
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
        <MemberManagement memberInformation={@state.member_information} gid={@props.gid} refresh={@refreshSettings}/>
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
        #Fine because @setState won't affect the next line
        @setState update @state, $set: emailDomain: ""
        update data, email_filter: $push: [@state.emailDomain]
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

TeacherManagement = React.createClass
  getInitialState: ->
    groups: []
    tabKey: 0

  onTabSelect: (tab) ->
    @setState update @state, tabKey: $set: tab

  componentWillMount: ->
    apiCall "GET", "/api/group/list"
    .done ((resp) ->
      @setState update @state, groups: $set: resp.data
    ).bind this

  render: ->
    <TabbedArea activeKey={@state.tabKey} onSelect={@onTabSelect}>
      {@state.groups.map ((group, i) ->
        <TabPane eventKey={i} key={i} tab={group.name}>
          <GroupManagement key={group.name} gid={group.gid}/>
        </TabPane>
      ).bind this}
    </TabbedArea>
$ ->
  React.render <TeacherManagement/>, document.getElementById("group-management")
