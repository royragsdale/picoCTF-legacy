renderShellServers = _.template($("#shell-servers-template").remove().text())

$ ->
  apiCall "GET", "/api/user/shell_servers", {}
  .done (data) ->
    if data.data
      $("#shell-servers").html renderShellServers({servers: data.data})
