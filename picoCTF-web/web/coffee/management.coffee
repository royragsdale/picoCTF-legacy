renderManagementTabs = _.template($("#management-tabs-template").remove().text())
renderProblemTab = _.template($("#problem-tab-template").remove().text())
renderProblem = _.template($("#problem-template").remove().text())
renderCategoryOptions = _.template($("#problem-category-options-template").remove().text())

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

refreshProblemList = ->
  $.when(( ->
    $("#problem-list").html renderProblemTab({
      renderProblem: renderProblem,
      problemFilter: (problem) ->
        _.all(f(problem) for f in [problemFilter, categoryFilter])
      problems: window.data.problems
  }))())
  .done () ->
    $(".problem-state").bootstrapSwitch()

setupQueueFrame = ->
  $("#main-content").prepend """
    <div class="col-md-2 fill-container" id="problem-aux-pane">
      <div id="problem-sort-options"></div>
      <div id="problem-category-options"></div>
    </div>
  """
  $("#main-content>.container").addClass("col-md-10")

$ ->
  $.when (
    setupQueueFrame()
    loadManagementBase()
    getProblemData()
  ).done () ->
    $("#problem-category-options").html renderCategoryOptions ({problems: window.data.problems})
    $(".problem-category-state").bootstrapSwitch()

    refreshProblemList()
    $("#problem-list").on "filterUpdate", () -> refreshProblemList()

    $(".problem-category-state").on "switchChange.bootstrapSwitch", () ->
      $("#problem-list").trigger "filterUpdate"

    $("#problem-search").on "input", () ->
      $("#problem-list").trigger "filterUpdate"
