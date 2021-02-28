<%
# user: user object, or None if new
# roles: all possible roles
# langs: all possible langs
if user is None:
  uname = rname = ""
  role_id = lang_id = 1
else:
  uname = user.username
  rname = user.realname
  role_id = user.role.id
  lang_id = user.lang.id
end
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
% if user is None:
  <title>{{_('New User')}}</title>
% else:
  <title>{{_('Edit User')}}</title>
% end
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", _=_, user=suser)
  <h1 class="centered">{{_('Edit')}}</h1>
% if user is None:
  <form action="/user_new" method="post">
% else:
  <form action="/user_upd/{{user.id}}" method="post">
% end
    <table class="field-list">
      <tbody>
        <tr>
          <td><label for="uname">{{_('Username')}}:</label></td>
          <td><input required class="flat-field" id="uname" name="uname" value="{{uname}}"></td>
        </tr>
        <tr>
          <td><label for="rname">{{_('Real Name')}}:</label></td>
          <td><input required class="flat-field" id="rname" name="rname" size="64" value="{{rname}}"></td>
        </tr>
        <tr>
          <td><label for="role">{{_('Role')}}:</label></td>
          <td>
            <select class="flat-field" id="role" name="role">
% for role in roles:
%   sel = "selected" if role.id == role_id else ""
              <option value="{{role.id}}" {{sel}}>{{_(role.desc)}}</option>
% end
            </select>
          </td>
        </tr>
        <tr>
          <td><label for="lang">{{_('Language')}}:</label></td>
          <td>
            <select class="flat-field" id="lang" name="lang">
% for lang in langs:
%   sel = "selected" if lang.id == lang_id else ""
              <option value="{{lang.id}}" {{sel}}>{{lang.name}}</option>
% end
            </select>
          </td>
        </tr>
      </tbody>
    </table>
    <br/><br/>
    <div class="button">
      <button class="flat-button" type="button" onclick="window.location='/users';">{{_('Cancel')}}</button>
      <button class="flat-button" type="submit">{{_('Save')}}</button>
    </div>
  </form>
</body>
</html>
