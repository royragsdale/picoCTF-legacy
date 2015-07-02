TabbedArea = ReactBootstrap.TabbedArea
TabPane = ReactBootstrap.TabPane

ManagementTabbedArea = React.createClass
  getInitialState: ->
    updates: []
    problems: []
    tabKey: 1

  onProblemChange: ->
    apiCall "GET", "/api/admin/problems"
    .done ((api) ->
      @setState React.addons.update @state,
        {problems: {$set: api.data}}
    ).bind this

  componentDidMount: ->
    # Formatting hack
    $("#main-content>.container").addClass("container-fluid")
    $("#main-content>.container").removeClass("container")

    @onProblemChange()

  onTabSelect: (tab) ->
    @setState React.addons.update @state,
      tabKey:
        $set: tab

  render: ->
      <TabbedArea activeKey={@state.tabKey} onSelect={@onTabSelect}>
        <TabPane eventKey={1} tab='Manage Problems'>
          <ProblemTab problems={@state.problems} onProblemChange={@onProblemChange}/>
        </TabPane>
        <TabPane eventKey={2} tab='Exceptions'>
          <ExceptionTab/>
        </TabPane>
        <TabPane eventKey={3} tab='Load Problems'>
          <ProblemLoaderTab/>
        </TabPane>
      </TabbedArea>

$ ->
  React.render <ManagementTabbedArea/>, document.getElementById("management-tabs")
