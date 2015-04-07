renderManagementTabs = _.template($("#management-tabs-template").remove().text())
renderProblemTab = _.template($("#problem-tab-template").remove().text())
renderProblem = _.template($("#problem-template").remove().text())

loadManagementBase = ->
  $("#management-tabs").html renderManagementTabs()

loadProblemManagementTab = ->
  apiCall "GET", "/api/admin/problems", {}
  .done (resp) ->
    switch resp["status"]
      when 1
        $("#problem-list").html renderProblemTab({
          renderProblem: renderProblem,
          problems: resp.data
        })

setupQueueFrame = ->
  $("#main-content").prepend('<div class="col-md-2" id="update-queue"></div>')
  $("#main-content>.container").addClass("col-md-10")

$ ->
  $.when (
    setupQueueFrame()
    loadManagementBase()
    loadProblemManagementTab()
    ( ->
      $(".problem-state").bootstrapSwitch()
    )()
  )
