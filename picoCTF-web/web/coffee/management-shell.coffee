Label = ReactBootstrap.Label
Input = ReactBootstrap.Input
Button = ReactBootstrap.Button
ButtonToolbar = ReactBootstrap.ButtonToolbar
Grid = ReactBootstrap.Grid
Row = ReactBootstrap.Row
Col = ReactBootstrap.Col
Well = ReactBootstrap.Well

ServerForm = React.createClass
  getInitialState: ->
    {shellServer: {"host":"", "port":"22", "username":"", "password":""}}

  componentDidMount: ->
    apiCall "GET", "/api/admin/shell_servers"
    .done ((api) ->
      if api.data.length == 0
        @setState {new: true, shellServer: @state.shellServer}
      else
        @setState {new: false, shellServer: api.data[0]}
    ).bind this

  addServer: ->
    apiCall "POST", "/api/admin/shell_servers/add", @state.shellServer
    .done (data) ->
      apiNotify data, "/management"

  deleteServer: ->
    apiCall "POST", "/api/admin/shell_servers/remove", {"sid": @state.shellServer.sid}
    .done (data) ->
      console.log(data)
      apiNotify data, "/management"

  updateServer: ->
    apiCall "POST", "/api/admin/shell_servers/update", @state.shellServer
    .done (data) ->
      apiNotify data

  loadProblems: ->
    apiCall "POST", "/api/admin/shell_servers/load_problems", {"sid": @state.shellServer.sid}
    .done (data) ->
      apiNotify data

  checkStatus: ->
    apiCall "GET", "/api/admin/shell_servers/check_status", {"sid": @state.shellServer.sid}
    .done (data) ->
      apiNotify data

  updateHost: (e) ->
    copy = @state.shellServer
    copy.host = e.target.value
    @setState {shellServer: copy}

  updatePort: (e) ->
    copy = @state.shellServer
    copy.port = e.target.value
    @setState {shellServer: copy}

  updateUsername: (e) ->
    copy = @state.shellServer
    copy.username = e.target.value
    @setState {shellServer: copy}

  updatePassword: (e) ->
    copy = @state.shellServer
    copy.password = e.target.value
    @setState {shellServer: copy}

  createFormEntry: (name, type, value, onChange) ->
    <Row>
      <Col md={2}>
        <h4 className="pull-right">{name}</h4>
      </Col>
      <Col md={10}>
        <Input className="form-control" type={type} value={value} onChange={onChange} />
      </Col>
    </Row>

  render: ->
    if @state.new
      buttons =
        <Button onClick={@addServer}>Add</Button>
    else
      buttons =
        <ButtonToolbar>
          <Button onClick={@updateServer}>Update</Button>
          <Button onClick={@deleteServer}>Delete</Button>
          <Button onClick={@loadProblems}>Load Deployment</Button>
          <Button onClick={@checkStatus}>Check Status</Button>
        </ButtonToolbar>

    <div>
      {@createFormEntry "Host", "text", @state.shellServer.host, @updateHost}
      {@createFormEntry "Port", "text", @state.shellServer.port, @updatePort}
      {@createFormEntry "Username", "text", @state.shellServer.username, @updateUsername}
      {@createFormEntry "Password", "password", @state.shellServer.password, @updatePassword}
      {buttons}
    </div>


ProblemLoaderTab = React.createClass
  getInitialState: ->
    {publishedJSON: ""}

  handleChange: (e) ->
    @setState {publishedJSON: e.target.value}

  pushData: ->
    apiCall "POST", "/api/problems/load_problems", {competition_data: @state.publishedJSON}
    .done ((data) ->
      apiNotify data, "/management"
    ).bind this

  clearPublishedJSON: ->
    @setState {publishedJSON: ""}

  render: ->
    publishArea =
    <div className="form-group">
      <h4>Paste your published JSON here:</h4>
      <Input className="form-control" type='textarea' rows="7"
        value={@state.publishedJSON} onChange={@handleChange}/>
    </div>

    <div>
      <Row>{publishArea}</Row>
      <Row>
        <ButtonToolbar>
          <Button onClick={@pushData}>Submit</Button>
          <Button onClick={@clearPublishedJSON}>Clear Data</Button>
        </ButtonToolbar>
      </Row>
    </div>

ShellServerTab = React.createClass

  render: ->
    <Well>
      <Grid>
        <Row>
          <h4>To add problems, either enter your shell server information on the left or paste your published JSON on the right.</h4>
        </Row>
        <Row>
          <Col md={5}>
            <ServerForm />
          </Col>
          <Col md={5} className="pull-right">
            <ProblemLoaderTab/>
          </Col>
        </Row>
      </Grid>
    </Well>
