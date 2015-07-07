TabbedArea = ReactBootstrap.TabbedArea
TabPane = ReactBootstrap.TabPane

ManagementTabbedArea = React.createClass
  getInitialState: ->
    tab = window.location.hash.substring(1)
    if tab == ""
      tab = "problems"

    updates: []
    problems: []
    tabKey: tab

  componentDidMount: ->
    # Formatting hack
    $("#main-content").prepend """
      <div class="col-md-2 fill-container" id="aux-pane"></div>
    """
    $("#main-content>.container").addClass("col-md-10")

    apiCall "GET", "/api/admin/problems"
    .done ((api) ->
      @setState React.addons.update @state,
        {problems: {$set: api.data}}
    ).bind this

  onTabSelect: (tab) ->
    @setState React.addons.update @state,
      tabKey:
        $set: tab

  render: ->
      <TabbedArea activeKey={@state.tabKey} onSelect={@onTabSelect}>
        <TabPane eventKey='problems' tab='Manage Problems'>
          <ProblemTab problems={@state.problems}/>
        </TabPane>
        <TabPane eventKey='exceptions' tab='Exceptions'>
          <ExceptionTab/>
        </TabPane>
        <TabPane eventKey='shell-servers' tab='Shell Server'>
          <ShellServerTab/>
        </TabPane>
        <TabPane eventKey='configuration' tab='Configuration'>
          <SettingsTab/>
        </TabPane>
      </TabbedArea>

$ ->
  React.render <ManagementTabbedArea/>, document.getElementById("management-tabs")
