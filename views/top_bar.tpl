  <div id="nav-bar">
    <a href="/">{{_('Home')}}</a>
% if user is not None and user.role.kind == "admin":
    <a href="/users">{{_('Users')}}</a>
% end
  </div>
  <div id="auth-bar">
% if user is None:
    <a href="/login">{{_('Login')}}</a>
% else:
    <strong>{{user.realname}}</strong>
    <a href="/logout">({{_('Logout')}})</a>
% end
  </div>
  <br/>
