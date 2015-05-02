ListGroupItem = ReactBootstrap.ListGroupItem
ListGroup = ReactBootstrap.ListGroup
Accordion = ReactBootstrap.Accordion
Panel = ReactBootstrap.Panel
Button = ReactBootstrap.Button
Glyphicon = ReactBootstrap.Glyphicon
Col = ReactBootstrap.Col
Badge = ReactBootstrap.Badge

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

  createRequestInfo: (request) ->
    if request
      <div>
        <h4>Browser information</h4>
        <p>Version: {request.browser} {request.browser_version}</p>
        <p>Platform: {request.platform}</p>
        <p>Address: {request.ip}</p>
      </div>
    else
      <p>No request information available.</p>

  createUserInfo: (user) ->
    if user
      <div>
        <h4>User information</h4>
        <p>Username: {user.username}</p>
        <p>Email: {user.email}</p>
        <p>Team: {user.team_name}</p>
      </div>
    else
      <p>No user information available.</p>

  createInfoDisplay: (exception) ->
    <div>
      <h3>Exception:</h3>
      <pre>{exception.trace}</pre>
      <Col xs={6}> {@createRequestInfo(exception.request)} </Col>
      <Col xs={6}> {@createUserInfo(exception.user)} </Col>
    </div>

  createExceptionItem: (exception, i) ->
    time =
    <small>
      {new Date(exception.time["$date"]).toUTCString()}
    </small>

    deleteButton =
    <Glyphicon onClick={@onDelete.bind this, exception} glyph="remove"/>

    occurencesBadge =
    <Badge>{exception.count}</Badge>

    exceptionHeader =
    <div>
      {exception.request.api_endpoint_method} <b>{exception.request.api_endpoint}</b>
      <div className="pull-right">
          {occurencesBadge} {time} {deleteButton}
      </div>
    </div>

    <Panel bsStyle="default" eventKey={i} key={i} header={exceptionHeader}>
      {@createInfoDisplay exception}
    </Panel>

  render: ->
    if @state.exceptions.length > 0
      groupedExceptions = _.groupBy @state.exceptions, (exception) -> exception.trace

      uniqueExceptions = _.map groupedExceptions, (exceptions, commonTrace) ->
        exception = _.first(exceptions)
        exception.count = exceptions.length
        return exception

      exceptionList = uniqueExceptions.map @createExceptionItem
      exceptionDisplay = <Accordion defaultActiveKey={0}> {exceptionList} </Accordion>

      <div>
        <h3>Displaying the {@state.exceptions.length} most recent exceptions.</h3>
        {exceptionDisplay}
      </div>
    else
      <div>
        <h3>No exceptions to display.</h3>
      </div>
