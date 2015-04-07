renderManagementTabs = _.template($("#management-tabs-template").remove().text())
renderProblemTab = _.template($("#problem-tab-template").remove().text())
renderProblem = _.template($("#problem-template").remove().text())
renderProblemOptions = _.template($("#problem-options-template").remove().text())

@data = {}

loadManagementBase = ->
  $("#management-tabs").html renderManagementTabs()

categoryFilter = (problem) ->
  categories = $(".problem-category-state")

  categoryReducer = (r, checkbox) ->
    categoryName = $(checkbox).data "category"
    active = $(checkbox).bootstrapSwitch "state"
    r[categoryName] = active
    return r

  activeCategories = _.reduce categories, categoryReducer, {}
  return activeCategories[problem.category]

problemFilter = (problem) ->
  nameNeedle = new RegExp $("#problem-search").val(), "i"
  return nameNeedle == "" or problem.name.search(nameNeedle) != -1

getProblemData = ->
  apiCall "GET", "/api/admin/problems", {}
  .done (resp) ->
    switch resp["status"]
      when 1
        window.data.problems = resp.data

loadProblemManagementTab = ->
  $.when(( ->
    if $("#problem-options").html() == ""
      $("#problem-options").html renderProblemOptions({problems: window.data.problems})

    $("#problem-list").html renderProblemTab({
      renderProblem: renderProblem,
      problemFilter: (problem) ->
        _.all(f(problem) for f in [problemFilter, categoryFilter])
      problems: window.data.problems
    }))()
  ).done () ->
    $(".problem-state").bootstrapSwitch()

setupQueueFrame = ->
  $("#main-content").prepend('<div class="col-md-2 fill-container" id="problem-aux-pane"><div id="problem-options"></div></div>')
  $("#main-content>.container").addClass("col-md-10")

$ ->
  $.when (
    setupQueueFrame()
    loadManagementBase()
    getProblemData()
  ).done () ->
    loadProblemManagementTab()
    $(".problem-category-state").bootstrapSwitch()
    $(".problem-category-state").on "switchChange.bootstrapSwitch", () ->
      loadProblemManagementTab()
    $("#problem-search").on "input", () -> loadProblemManagementTab()
