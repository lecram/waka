<%
# users: users
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{_('Users')}}</title>
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", _=_, user=suser)
  <div class="content">
    <h1 class="centered">{{_('Users')}}</h1>
    <table class="link-list">
      <thead>
        <tr>
          <th>{{_('User')}}</th><th>{{_('Name')}}</th><th>{{_('Role')}}</th><th>{{_('Actions')}}</th>
        </tr>
      </thead>
      <tbody>
% for user in users:
        <tr>
          <td>{{user.username}}</td>
          <td>{{user.realname}}</td>
          <td>{{_(user.role.desc)}}</td>
          <td>
            <a href="{{'/user/edit/{}'.format(user.username)}}">{{_('Edit')}}</a>
            <a href="{{'/user/pass/{}'.format(user.username)}}">{{_('Password')}}</a>
          </td>
        </tr>
% end
      </tbody>
    </table>
    <p><a href="/user/new">{{_('New User')}}</a></p>
  </div>
</body>
</html>
