Row = ReactBootstrap.Row
Input = ReactBootstrap.Input
Col = ReactBootstrap.Col
Button = ReactBootstrap.Button
ButtonToolbar = ReactBootstrap.ButtonToolbar

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
      <h3>Paste your published json here:</h3>
      <Input className="form-control" type='textarea' rows="20"
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
