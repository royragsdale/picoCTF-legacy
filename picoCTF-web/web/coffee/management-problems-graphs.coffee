ProblemSubmissionDoughnut = React.createClass
  componentDidMount: ->
    if @props.visible
      ctx = @getDOMNode().getContext "2d"
      data = [
        {
          value: @props.invalid
          color:"#F7464A"
          highlight: "#FF5A5E"
          label: "Invalid submissions"
        },
        {
          value: @props.valid
          color: "#46BFBD"
          highlight: "#5AD3D1"
          label: "Valid submissions"
        }
      ]

      (new Chart ctx).Doughnut data,
        animateRotate: false

  render: ->
    style =
      padding: 0
      margin: "auto"
      display: "block"

    <canvas height="200" width="200" style={style}/>
