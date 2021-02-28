<%
# page: page object
# html_text: page text as HTML
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{page.title}}</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", _=_, user=suser)
  <a href="/edit/{{page.name}}">{{_('Edit')}}</a>
  <a href="/log/{{page.name}}">{{_('History')}}</a>
  <a href="/src/{{page.name}}">{{_('Source')}}</a>
  <h1 class="centered">{{page.title}}</h1>
  <div class="page">{{!html_text}}</div>
</body>
</html>
