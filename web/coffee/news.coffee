window.load_news = ->
  $.ajax(type: "GET", cache: false, url: "/api/news")
  .done (data) ->
      html = ''
      months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
      for d in data
        html += '<h3>' + d['header']
        try
          raw_date_string = d['date'];
          date_string = raw_date_string.split(" ")[0]
          date = new Date(Date.parse(date_string))
          day = date.getDate()
          month = date.getMonth()
          year = date.getFullYear()
          html += ' - ' + String(months[month] + ' ' + day + ', ' + year)
        html += '</h3>'
        html += '<div class="news_article">' + d['articlehtml'] + '</div>'
      $("#news_holder").html html