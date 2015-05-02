TabbedArea = ReactBootstrap.TabbedArea
TabPane = ReactBootstrap.TabPane

ManagementTabbedArea = React.createClass
  render: ->
      <TabbedArea defaultActiveKey={2}>
            <TabPane eventKey={1} tab='Problems'>Problems</TabPane>
            <TabPane eventKey={2} tab='Exceptions'>
              <ExceptionTab/>
            </TabPane>
      </TabbedArea>

$ ->
  React.render <ManagementTabbedArea/>, document.getElementById("management-tabs")
