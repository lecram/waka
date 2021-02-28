<%
# page: page object
# versions: versions of the page, ordered from the most recent
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{page.name}} - {{_('History')}}</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", _=_, user=suser)
  <h1 class="centered">{{_('Versions')}}</h1>
  <h2 class="centered">{{page.title}}</h2>
  <table class="link-list">
    <thead>
      <tr>
        <th>#</th><th>{{_('Date')}}</th><th>{{_('Author')}}</th><th>{{_('Message')}}</th>
      </tr>
    </thead>
    <tbody>
% for version in versions:
%   page_ver = "{}/{}".format(page.name, version.num)
      <tr>
        <td><a href="{{'/p/{}'.format(page_ver)}}">{{version.num}}</a></td>
        <td>{{version.date}}</td>
        <td>{{version.author.realname}}</td>
        <td><a href="{{'/diff/{}'.format(page_ver)}}">{{version.msg}}</a></td>
      </tr>
% end
    </tbody>
  </table>
</body>
</html>
