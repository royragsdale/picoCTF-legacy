renderManagementTabs = _.template($("#management-tabs-template").remove().text())
renderProblemTab = _.template($("#problem-tab-template").remove().text())
renderProblem = _.template($("#problem-template").remove().text())
renderCategoryOptions = _.template($("#problem-category-options-template").remove().text())
renderUpdateQueue = _.template($("#problem-update-queue-template").remove().text())

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
      <div class="update-queue" id="problem-update-queue"></div>
    </div>
  """

  $("#problem-update-queue").on "makeChange", (e, data) ->
    if @changes == undefined
      @changes = []

    if data.shouldAdd @changes
      @changes.push data

    $(this).html renderUpdateQueue {changes: @changes}
    $("#process-problem-queue-button").on "click", (e) ->
      $("#problem-update-queue").trigger "processChanges"

  $("#problem-update-queue").on "processChanges", () ->
    console.log "Processing"
    _.each @changes, (change) ->
      change.process()
    refreshProblemList()

  $("#main-content>.container").addClass("col-md-10")

problemStateChanges = ->
  $(".problem-state").on "switchChange.bootstrapSwitch", (e, state) ->
    pid = $(e.target).attr "id"
    problem = window.data.problems[pid]
    change = {
      type: "availability"
      target: problem.name
      data: {original: !state, change: state}
      display: (if state then "Enabling" else "Disabling") + " " + problem.name  + " for the competition."
      shouldAdd: (changes) -> _.all (_.map changes, (change) ->
        !(change.target == problem.name and change.type == "availability"))
      process: () ->
        apiCall "POST", "/api/admin/problems/availability", {pid: problem.pid, state: state}
    }

    $("#problem-update-queue").trigger "makeChange", [change]

$ ->
  $.when (
    setupQueueFrame()
    loadManagementBase()
    getProblemData()
  ).done () ->

    $("#problem-category-options").html renderCategoryOptions ({problems: window.data.problems})
    refreshProblemList()

    $(".problem-category-state").bootstrapSwitch()
    $("#problem-list").on "filterUpdate", () -> refreshProblemList()

    $(".problem-category-state").on "switchChange.bootstrapSwitch", () ->
      $("#problem-list").trigger "filterUpdate"

    problemStateChanges()

    $("#problem-search").on "input", () ->
      $("#problem-list").trigger "filterUpdate"
