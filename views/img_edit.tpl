<%
# img: img object, or None if new
if img is None:
  path = desc = ""
else:
  path = img.path
  desc = img.desc
end
%>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
% if img is None:
  <title>{{_('New Image')}}</title>
% else:
  <title>{{_('Edit Image')}}</title>
% end
  <link href="/static/style.css" rel="stylesheet" type="text/css">
</head>
<body>
% include("top_bar", _=_, user=suser)
  <h1 class="centered">{{_('Edit')}}</h1>
% if img is None:
  <form action="/img_new" method="post" enctype="multipart/form-data">
% else:
  <form action="/img_upd/{{img.id}}" method="post"  enctype="multipart/form-data">
% end
    <table class="field-list">
      <tbody>
        <tr>
          <td><label for="path">{{_('Path')}}:</label></td>
          <td><input required class="flat-field" id="path" name="path" size="32" value="{{path}}"></td>
        </tr>
        <tr>
        <tr>
          <td><label for="desc">{{_('Description')}}:</label></td>
          <td><input required class="flat-field" id="desc" name="desc" size="128" value="{{desc}}"></td>
        </tr>
        <tr>
          <td><label for="fname">{{_('File')}}:</label></td>
          <td><input type="file" required class="flat-field" id="fname" name="fname" accept="image/png, image/jpeg"></td>
        </tr>
      </tbody>
    </table>
    <br/><br/>
    <div class="button">
      <button class="flat-button" type="button" onclick="window.location='/imgs';">{{_('Cancel')}}</button>
      <button class="flat-button" type="submit">{{_('Save')}}</button>
    </div>
  </form>
</body>
</html>
