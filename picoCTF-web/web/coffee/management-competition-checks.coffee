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

    elapsedDisplay = "..."
    if @props.elapsed
      elapsedDisplay = "#{parseFloat(@props.elapsed).toFixed(1)} secs"

    <ListGroupItem>
      <h4>
        <Glyphicon glyph={glyphName} className={glyphStyle}/> {@props.name} <span className="pull-right">{elapsedDisplay}</span>
      </h4>
    </ListGroupItem>

TestGroup = React.createClass
  getInitialState: ->
    state = {}
    _.map @props.tests, (test) ->
      state[test.name] = test
      state[test.name].status = "waiting"
      state[test.name].start = Date.now()
    state

  updateTestState: (testName, status) ->
    updateObject = {}
    updateObject[testName] =
      status: $set: status
      elapsed: $set: (Date.now() - @state[testName].start) / 1000.0 #seconds
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
    <Panel>
      <ListGroup fill>
        {_.map _.values(@state), (test, i) ->
          <TestGroupItem key={i} {...test}/>}
      </ListGroup>
    </Panel>

CompetitionCheck = React.createClass

  getInitialState: ->
    competitionReadiness: "waiting"

  alwaysTrue: (t, setStatus) ->
    setTimeout (setStatus.bind null, t), (Math.random() * 3000)

  onStatusChange: (status) ->
    @setState update @state,
      competitionReadiness: $set: status

  render: ->
    sanityChecks = [
      {name: "Just Checking 1", func: @alwaysTrue.bind null, "passing"}
      {name: "Just Checking 2", func: @alwaysTrue.bind null, "passing"}
      {name: "Just Checking 3", func: @alwaysTrue.bind null, "passing"}
    ]

    <div>
      <h3>Competition Status: <b>{@state.competitionReadiness}</b></h3>
      <Col md={6} className="hard-right">
        <TestGroup tests={sanityChecks} onStatusChange={@onStatusChange}/>
      </Col>
    </div>
