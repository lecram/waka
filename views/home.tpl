<%
# pages: list of pages
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Wiki</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", _=_, user=suser)
  <h1 class="centered">Wiki</h1>
  <ul>
% for page in pages:
    <li><a href="/p/{{page.name}}">{{page.title}}</a></li>
% end
  </ul>
  <p><a href="/new">{{_("New Page")}}</a></p>
</body>
</html>
