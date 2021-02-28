<%
# version: version object
# html_table: diff table as HTML
page = version.page
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{page.name}} - {{_('Diff')}}</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", _=_, user=suser)
  <a href="/log/{{page.name}}">{{_('History')}}</a>
  <h1 class="centered">{{version.num}} - {{version.msg}}</h1>
  <div class="diff">{{!html_table}}</div>
</body>
</html>
