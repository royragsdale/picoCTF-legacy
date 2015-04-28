ListGroupItem = ReactBootstrap.ListGroupItem
ListGroup = ReactBootstrap.ListGroup
Accordion = ReactBootstrap.Accordion
Panel = ReactBootstrap.Panel
Button = ReactBootstrap.Button
Glyphicon = ReactBootstrap.Glyphicon
Col = ReactBootstrap.Col

ExceptionTab = React.createClass
  getInitialState: ->
    {exceptions: []}

  componentDidMount: ->
    apiCall "GET", "/api/admin/exceptions", {limit: 20}
    .done ((api) ->
      @setState {exceptions: api.data}
     ).bind this

  onDelete: (exception) ->
    #Should call out and "hide" the exception. Currently just temporarily removes it.
    newExceptions = _.reject @state.exceptions, (item) -> item == exception
    @setState {exceptions: newExceptions}

  createInfoDisplay: (exception) ->
    request = exception.request
    user = exception.user

    <div>
      <Col xs={6}>
        <h4>Browser information</h4>
        <p>Version: {request.browser} {request.browser_version}</p>
        <p>Platform: {request.platform}</p>
        <p>Address: {request.ip}</p>
      </Col>
      <Col xs={6}>
        <h4>User information</h4>
        <p>Username: {user.username}</p>
        <p>Email: {user.email}</p>
        <p>Team: {user.team_name}</p>
      </Col>
    </div>

  createExceptionItem: (exception, i) ->
    time =
    <small>
      {new Date(exception.time["$date"]).toUTCString()}
    </small>

    deleteButton =
    <Button className="pad" bsSize="xsmall" onClick={@onDelete.bind this, exception}>
      <Glyphicon glyph="remove"/>
    </Button>

    exceptionHeader =
    <div>
      {exception.request.api_endpoint_method} <b>{exception.request.api_endpoint}</b>
      <div className="pull-right">
          {time} {deleteButton}
      </div>
    </div>

    exceptionBody =
    <div>
      <h3>Exception:</h3>
      <pre>{exception.trace}</pre>
    </div>

    style = if i == 0 then "warning" else "info"

    <Panel bsStyle={style} eventKey={i} key={i} header={exceptionHeader}>
      {exceptionBody}
      {@createInfoDisplay exception}
    </Panel>

  render: ->
    exceptionList = @state.exceptions.map @createExceptionItem
    exceptionDisplay = <Accordion defaultActiveKey={0}> {exceptionList} </Accordion>

    <div>
      <h3>Displaying the {@state.exceptions.length} most recent exceptions.</h3>
      {exceptionDisplay}
    </div>
