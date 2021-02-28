<%
# page: page object, or None if new
# text: current text for the page
if page is None:
  name = title = ""
  back = "/"
else:
  name = page.name
  title = page.title
  back = "/p/" + name
end
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
% if page is None:
  <title>{{_('New Page')}}</title>
% else:
  <title>{{page.name}} - {{_('Edit')}}</title>
% end
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", _=_, user=suser)
  <h1 class="centered">{{_('Edit')}}</h1>
% if page is None:
  <form action="/new" method="post">
% else:
  <form action="/upd/{{page.id}}" method="post">
% end
    <table class="field-list">
      <tbody>
        <tr>
          <td><label for="name">{{_('Name')}}:</label></td>
          <td><input required class="flat-field" id="name" name="name" value="{{name}}"></td>
        </tr>
        <tr>
          <td><label for="title">{{_('Title')}}:</label></td>
          <td><input required class="flat-field" id="title" name="title" size="64" value="{{title}}"></td>
        </tr>
        <tr>
          <td><label for="text">{{_('Text')}}:</label></td>
          <td><textarea required cols="100" rows="20" class="flat-field" id="text" name="text">{{!text}}</textarea></td>
        </tr>
% if page is None:
        <tr>
          <td><label for="private">{{_('Private')}}:</label></td>
          <td><input type="checkbox" class="flat-field" id="private" name="private" checked></td>
        </tr>
% else:
        <tr>
          <td><label for="message">{{_('Message')}}:</label></td>
          <td><input class="flat-field" id="message" name="message" size="64" value=""></td>
        </tr>
% end
      </tbody>
    </table>
    <br/><br/>
    <div class="button">
      <button class="flat-button" type="button" onclick="window.location='{{back}}';">{{_('Cancel')}}</button>
      <button class="flat-button" type="submit">{{_('Save')}}</button>
    </div>
  </form>
</body>
</html>
