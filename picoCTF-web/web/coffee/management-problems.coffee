Panel = ReactBootstrap.Panel
Button = ReactBootstrap.Button
ButtonGroup = ReactBootstrap.ButtonGroup
Glyphicon = ReactBootstrap.Glyphicon
Col = ReactBootstrap.Col
Input = ReactBootstrap.Input
Label = ReactBootstrap.Label
PanelGroup = ReactBootstrap.PanelGroup
Row = ReactBootstrap.Row
ListGroup = ReactBootstrap.ListGroup
ListGroupItem = ReactBootstrap.ListGroupItem

update = React.addons.update

SortableButton = React.createClass
  propTypes:
    name: React.PropTypes.string.isRequired

  getInitialState: ->
    ascending: true
    focused: false

  #TODO: Needs reworked.
  handleClick: (e) ->
    if not @state.focused and false
      @setState update @state,
        focused: $set: true
    else
      @setState update @state,
        ascending: $set: !@state.ascending

     @props.onSortChange @props.name, !@state.ascending

  render: ->
    glyph = if @state.ascending then <Glyphicon glyph="chevron-up"/> else <Glyphicon glyph="chevron-down"/>
    <Button active={@props.active} onClick={@handleClick}>{@props.name} {glyph}</Button>

ProblemFilter = React.createClass
  propTypes:
    onFilterChange: React.PropTypes.func.isRequired
    filter: React.PropTypes.string

  getInitialState: ->
    filter: @props.filter

  onChange: ->
    filterValue = this.refs.filter.getInputDOMNode().value
    @setState {filter: filterValue}
    @props.onFilterChange filterValue

  render: ->
    glyph = <Glyphicon glyph="search"/>
    <Panel>
      <Col xs={12}>
        Search
        <Input type='text' className="form-control"
          ref="filter"
          addonBefore={glyph}
          onChange={@onChange}
          value={@state.filter}/>
      </Col>
      <Col xs={12}>
        <SortableButton name="score" onSortChange={@props.onSortChange}/>
        <SortableButton name="name" onSortChange={@props.onSortChange}/>
        <SortableButton name="category" onSortChange={@props.onSortChange}/>
      </Col>
    </Panel>

ProblemClassifierList = React.createClass
  render: ->
    categories = _.groupBy @props.problems, "category"
    categoryData = _.map categories, (problems, category) ->
      name: "Only #{category} problems"
      size: problems.length
      classifier: (problem) ->
        problem.category == category

    organizations = _.groupBy @props.problems, "organization"
    organizationData = _.map organizations, (problems, organization) ->
      name: "Created by #{organization}"
      size: problems.length
      classifier: (problem) ->
        problem.organization == organization

    <PanelGroup className="problem-classifier" collapsible>
      <ProblemClassifier name="Categories" data={categoryData} {...@props}/>
      <ProblemClassifier name="Organizations" data={organizationData} {...@props}/>
      <ProblemClassifier name="Bundles" data={[]} {...@props}/>
    </PanelGroup>

ClassifierItem = React.createClass
  getInitialState: ->
    active: false

  handleClick: (e) ->
    activeState = !@state.active
    @setState {active: activeState}
    console.log @props, activeState
    @props.setClassifier activeState, @props.classifier

  render: ->
    glyph = <Glyphicon glyph="ok"/>

    <ListGroupItem onClick={@handleClick}>
        {@props.name} {if @state.active then glyph} <div className="pull-right"><Badge>{@props.size}</Badge></div>
    </ListGroupItem>

ProblemClassifier = React.createClass
  render: ->
    <Panel header={@props.name} defaultExpanded collapsible>
      <ListGroup fill>
        {@props.data.map ((data, i) ->
          <ClassifierItem key={i+data} setClassifier={@props.setClassifier} {...data}/>
        ).bind this}
      </ListGroup>
    </Panel>

Problem = React.createClass
  getInitialState: ->
    disabled: @props.disabled

  onStateToggle: (e) ->
    apiCall "POST", "/api/admin/problems/availability", {pid: @props.pid, state: !@state.disabled}
    .done ((api) ->
      if api.status == 1
        @setState update @state,
          disabled: $set: !@state.disabled
    ).bind this

  render: ->
    statusButton =
    <Button bsSize="xsmall" onClick={@onStateToggle}>
      {if @state.disabled then "Enable" else "Disable"}
    </Button>

    problemHeader =
    <div>
      {@props.category} - {@props.name}
      <div className="pull-right">
        {statusButton}
      </div>
    </div>

    problemFooter = @props.tags.map (tag, i) ->
      <Label key={i}><a href="#">{tag}</a></Label>

    panelStyle = if @state.disabled then "default" else "info"

    <Panel bsStyle={panelStyle} header={problemHeader} footer={problemFooter}>
      <h4>Score: {@props.score}</h4>
      <pre>
        <code>
          {@props.description}
        </code>
      </pre>
    </Panel>

ProblemList = React.createClass
  propTypes:
    problems: React.PropTypes.array.isRequired

  render: ->
    if @props.problems.length == 0
      return <h4>No problems have been loaded. Click <a href='#'>here</a> to get started.</h4>

    problemComponents = @props.problems.map (problem, i) ->
      <Col xs={6} lg={4} key={i}>
        <Problem {...problem}/>
      </Col>

    <div>
      {problemComponents}
    </div>

ProblemTab = React.createClass
  propTypes:
    problems: React.PropTypes.array.isRequired

  getInitialState: ->
    filterRegex: /.*/
    activeSort:
      name: "score"
      ascending: true
    problemClassifier: (problem) -> true

  onFilterChange: (filter) ->
    try
      newFilter = new RegExp(filter)
      @setState update @state,
        filterRegex: $set: newFilter
    catch
      # We shouldn't do anything.

  onSortChange: (name, ascending) ->
    @setState update @state,
      activeSort: $set: {name: name, ascending: ascending}

  setClassifier: (classifierState, classifier) ->
    if not classifierState
      classifier = (problem) -> true

    @setState update @state,
      problemClassifier: $set: classifier

  filterProblems: (problems) ->
    visibleProblems = _.filter problems, ((problem) ->
      (@state.filterRegex.exec problem.name) != null and @state.problemClassifier problem
    ).bind this

    sortedProblems = _.sortBy visibleProblems, @state.activeSort.name
    if @state.activeSort.ascending
      sortedProblems
    else
      sortedProblems.reverse()

  render: ->
    filteredProblems = @filterProblems @props.problems
    <Row className="pad">
      <Col xs={3} md={3}>
        <Row>
          <ProblemFilter onSortChange={@onSortChange} filter="" onFilterChange={@onFilterChange}/>
        </Row>
        <Row>
          <ProblemClassifierList setClassifier={@setClassifier} problems={filteredProblems}/>
        </Row>
      </Col>
      <Col xs={9} md={9}>
        <ProblemList problems={filteredProblems}/>
      </Col>
    </Row>
