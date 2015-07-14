Tooltip = ReactBootstrap.Tooltip
OverlayTrigger = ReactBootstrap.OverlayTrigger
Input = ReactBootstrap.Input
Row = ReactBootstrap.Row
Col = ReactBootstrap.Col
Button = ReactBootstrap.Button

Hint = React.createClass
  propTypes:
    text: React.PropTypes.string.isRequired

  render: ->
    tooltip = <Tooltip>{@props.text}</Tooltip>
    <OverlayTrigger placement="top" overlay={tooltip}>
      <Glyphicon className="pad" glyph="question-sign" style={fontSize:"0.8em"}/>
    </OverlayTrigger>

FormEntry = React.createClass
  propTypes:
    name: React.PropTypes.string.isRequired
    entry: React.PropTypes.func.isRequired
    description: React.PropTypes.string

  render: ->
    if @props.description
      hint = <Hint text={@props.description} />
    else
      hint = ""

    <Row>
      <Col md={4}>
        <h4 className="pull-right">
          {hint}
          {@props.name}
        </h4>
      </Col>
      <Col md={8}>
        {@props.entry}
      </Col>
    </Row>

TextEntry = React.createClass
  propTypes:
    name: React.PropTypes.string.isRequired
    value: React.PropTypes.string.isRequired
    type: React.PropTypes.string.isRequired
    onChange: React.PropTypes.func.isRequired

  render: ->
    input = <Input className="form-control" type={@props.type} value={@props.value} onChange={@props.onChange} />
    <FormEntry entry={input} {...@props} />

BooleanEntry = React.createClass
  propTypes:
    name: React.PropTypes.string.isRequired
    value: React.PropTypes.bool.isRequired
    onChange: React.PropTypes.func.isRequired

  render: ->
    button = <Button bsSize="xsmall" onClick=@props.onChange>{if @props.value then "Enabled" else "Disabled"}</Button>
    <FormEntry entry={button} {...@props} />

TimeEntry = React.createClass
  propTypes:
    name: React.PropTypes.string.isRequired
    value: React.PropTypes.number.isRequired
    onChange: React.PropTypes.func.isRequired

  componentDidMount: ->
    date = new Date(@props.value)
    node = React.findDOMNode(@refs.datetimepicker)
    $(node).datetimepicker
      defaultDate: date
      inline: true,
      sideBySide: true
    .on "dp.change", ((e) ->
      @props.onChange e.date.toDate().getTime()
    ).bind(this)

  render: ->
    timepicker = <Panel> <div ref="datetimepicker"></div> </Panel>
    <FormEntry entry={timepicker} {...@props} />
