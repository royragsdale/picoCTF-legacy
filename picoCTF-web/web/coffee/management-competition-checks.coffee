ListGroupItem = ReactBootstrap.ListGroupItem
ListGroup = ReactBootstrap.ListGroup
Accordion = ReactBootstrap.Accordion
Panel = ReactBootstrap.Panel
Button = ReactBootstrap.Button
Glyphicon = ReactBootstrap.Glyphicon
Col = ReactBootstrap.Col
Badge = ReactBootstrap.Badge

update = React.addons.update

TestGroupItem = React.createClass
  render: ->
    glyphName = "asterik"
    glyphStyle = ""

    switch @props.status
      when "waiting"
        glyphName = "refresh"
        glyphStyle = "spin"
      when "failing"
        glyphName = "remove"
      when "passing"
        glyphName = "ok"

    <ListGroupItem>{@props.name} <Glyphicon glyph={glyphName} className={glyphStyle}/></ListGroupItem>

TestGroup = React.createClass
  getInitialState: ->
    state = {}
    _.map @props.tests, (test) ->
      state[test.name] = test
      state[test.name].status = "waiting"
    state

  updateTestState: (testName, status) ->
    updateObject = {}
    updateObject[testName] =
      status: $set: status
    newState = update @state, updateObject

    totalStatus = "passing"
    if _.any(newState, (test) -> test.status == "waiting")
      totalStatus = "waiting"
    else if _.any(newState, (test) -> test.status == "failing")
      totalStatus = "failing"

    @setState newState
    @props.onStatusChange totalStatus

  componentWillMount: ->
    #Initiate all the tests with the updateTestState callback
    _.each @state, ((test, testName) ->
      test.func (@updateTestState.bind null, testName)
    ).bind this

  render: ->
    <ListGroup fill>
      {_.map @state, (test, i) ->
        <TestGroupItem key={i} {...test}/>}
    </ListGroup>

CompetitionCheck = React.createClass

  getInitialState: ->
    competitionReadiness: "waiting"

  alwaysTrue: (t, setStatus) ->
    setTimeout (setStatus.bind null, t), (Math.random() * 3000)

  checkEnabledProblems: (setStatus) ->
    apiCall "GET", "/api/admin/problems"
    .done (result) ->
      status = "failing"
      for problem in result.data.problems
        if problem.disabled == false
          status = "passing"
          break

      setStatus status


  checkProblemsAlive: (setStatus) ->
    apiCall "GET", "/api/admin/shell_servers"
    .done (api) ->
      status = "passing"
      servers = api.data

      if servers.length is 0
        status = "failing"

      apiCalls = $.map(servers, (server) -> apiCall "GET", "/api/admin/shell_servers/check_status", {sid: server.sid})
      ($.when).apply(this, apiCalls).done () ->
        for result in $.map(arguments, _.first)
          if result.status is 0
            status = "failing"
        setStatus status

  checkDownloadsAccessible: (setStatus) ->
    apiCall "GET", "/api/admin/problems"
    .done (result) ->
      status = "passing"
      requests = []
      for problem in result.data.problems
        for instance in problem.instances
          $("<p>"+instance.description+"</p>").find("a").each (i, a) ->
            url = $(a).attr("href")
            requests.push($.ajax({url: url, dataType: 'text', type: 'GET'}))

      ($.when).apply(this, apiCalls).done () ->
        for result in arguments
          if result.status is 404
            status = "failing"

        setStatus status


  onStatusChange: (status) ->
    @setState update @state,
      competitionReadiness: $set: status

  render: ->
    sanityChecks = [
      {name: "Check Enabled Problems", func: @checkEnabledProblems}
      {name: "Problems Alive on Shell Server", func: @checkProblemsAlive}
      #{name: "Problem Downloads Accessible", func: @checkDownloadsAccessible}
    ]

    <div>
      <h4>Competition Status {@state.competitionReadiness}</h4>
      <TestGroup tests={sanityChecks} onStatusChange={@onStatusChange}/>
    </div>
