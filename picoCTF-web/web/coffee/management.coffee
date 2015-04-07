renderManagementTabs = _.template($("#management-tabs-template").remove().text())
renderProblemTab = _.template($("#problem-tab-template").remove().text())
renderProblem = _.template($("#problem-template").remove().text())

loadManagementBase = ->
  $("#management-tabs").html renderManagementTabs()

problemFilter = (problem) ->
  nameNeedle = new RegExp $("#problem-search").val(), "i"
  return _.all [nameNeedle == "" or problem.name.search(nameNeedle) != -1]

loadProblemManagementTab = ->
  apiCall "GET", "/api/admin/problems", {}
  .done (resp) ->
    switch resp["status"]
      when 1
        $("#problem-list").html renderProblemTab({
          renderProblem: renderProblem,
          problemFilter: problemFilter,
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
      $("#problem-search").on "input", () -> loadProblemManagementTab()
      $(".problem-state").bootstrapSwitch()
    )()
  )
