import re

from bottle import view, static_file, hook, route, run, request, response, redirect, template
import markdown2

from model import *
import trans

link = re.compile(r'(#\w+)')
md_extras = ("break-on-newline code-friendly fenced-code-blocks "
             "header-ids strike tables task_list").split()

t = trans.Trans()
t.scan_langs()

def render(text):
    frags = link.split(text)
    is_link = False
    md = ""
    for frag in frags:
        if is_link:
            name = frag[1:]
            page = Page.get_or_none(Page.name == name)
            title = page and page.title or "???"
            md += '[{0}](/p/{0} "{1}")'.format(name, title)
        else:
            md += frag
        is_link = not is_link
    return markdown2.markdown(md, extras=md_extras)

def get_session():
    key = request.cookies.get('key', "")
    return Session.get_or_none(Session.key == key)

def can_read(session, page):
    return page is not None and (session is not None or not page.private)

def can_write(session):
    return session is not None and session.user.role.kind in ("writer", "admin")

def can_admin(session):
    return session is not None and session.user.role.kind == "admin"

def lang_code(session, request, available, default="en"):
    if session is not None:
        return session.user.lang.code
    accept_language = request.headers.get("Accept-Language", "")
    accept_language = accept_language.replace(" ", "")
    pairs = []
    for acc in accept_language.split(','):
        sp = acc.split(";q=")
        if len(sp) == 2:
            pairs.append(sp)
        else:
            pairs.append((acc, "1"))
    pairs.sort(key=lambda p: float(p[1]), reverse=True)
    locales = [p[0] for p in pairs]
    for locale in locales:
        for lang in available:
            if locale[:2].lower() == lang[:2].lower():
                return lang
    return default

def get_underline(session, request):
    code = lang_code(session, request, t.langs.keys())
    return t.get_underline(code)

@hook('before_request')
def _connect_db():
    db.connect()

@hook('after_request')
def _close_db():
    if not db.is_closed():
        db.close()

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static/')

@route('/')
@view('home')
def home():
    session = get_session()
    if session is None:
        pages = Page.select().where(~Page.private)
    else:
        pages = Page.select()
    suser = getattr(session, "user", None)
    _ = get_underline(session, request)
    return dict(_=_, pages=pages, suser=suser)

@route('/login')
@view('login')
def show_login():
    session = get_session()
    if session is not None:
        redirect('/')
    else:
        _ = get_underline(session, request)
        return dict(_=_)

@route('/login', method='POST')
def try_to_login():
    username = request.forms.username
    password = request.forms.password
    session = login(username, password)
    if session is not None:
        ts = datetime.datetime.now() + SESSION_MAX_AGE
        response.set_cookie('key', session.key, expires=ts)
    redirect('/login')

@route('/logout')
def logout():
    session = get_session()
    if session is not None:
        response.delete_cookie('key')
        session.delete_instance()
    redirect('/')

@route('/users')
@view('users')
def show_users():
    session = get_session()
    if not can_admin(session):
        redirect('/')
    _ = get_underline(session, request)
    return dict(_=_, users=User.select(), suser=session.user)

@route('/user/pass/<name>')
@view('user_pass')
def user_pass(name):
    user = User.get_or_none(User.username == name)
    session = get_session()
    if None in (session, user):
        redirect('/users')
    if user != session.user and not can_admin(session):
        redirect('/users')
    _ = get_underline(session, request)
    return dict(_=_, user=user, suser=session.user)

@route('/user_pass/<_id:int>', method='POST')
def post_user_padd(_id):
    user = User.get_by_id(_id)
    session = get_session()
    if None in (session, user):
        redirect('/users')
    if user != session.user and not can_admin(session):
        redirect('/users')
    oldpass = request.forms.oldpass
    newpass = request.forms.newpass
    if request.forms.newpassconfirm != newpass:
        redirect('/user/pass/{}'.format(user.username))
    if not user.test_password(oldpass):
        redirect('/user/pass/{}'.format(user.username))
    pw_hash, pw_salt = hash_password(newpass)
    user.passhash = pw_hash
    user.passsalt = pw_salt
    user.save()
    redirect('/users')

@route('/user/new')
@view('user_edit')
def user_new():
    session = get_session()
    if not can_admin(session):
        redirect('/')
    roles = Role.select()
    langs = Lang.select()
    _ = get_underline(session, request)
    return dict(_=_, user=None, roles=roles, langs=langs, suser=session.user)

@route('/user/edit/<name>')
@view('user_edit')
def user_edit(name):
    session = get_session()
    if not can_admin(session):
        redirect('/')
    user = User.get_or_none(User.username == name)
    if user is None:
        redirect('/')
    roles = Role.select()
    langs = Lang.select()
    _ = get_underline(session, request)
    return dict(_=_, user=user, roles=roles, langs=langs, suser=session.user)

@route('/user_new', method='POST')
def post_user_new():
    session = get_session()
    if not can_admin(session):
        redirect('/')
    uname = request.forms.uname
    rname = request.forms.rname
    role_id = request.forms.role
    role = Role.get_by_id(role_id)
    lang_id = request.forms.lang
    lang = Lang.get_by_id(lang_id)
    new_user(uname, rname, "", role, lang)
    redirect('/users')

@route('/user_upd/<_id:int>', method='POST')
def post_user_upd(_id):
    session = get_session()
    if not can_admin(session):
        redirect('/')
    user = User.get_by_id(_id)
    user.username = request.forms.uname
    user.realname = request.forms.rname
    role_id = request.forms.role
    user.role = Role.get_by_id(role_id)
    lang_id = request.forms.lang
    user.lang = Lang.get_by_id(lang_id)
    user.save()
    redirect('/users')

@route('/p/<name>')
@view('page')
def show_page(name):
    session = get_session()
    page = Page.get_or_none(Page.name == name)
    if not can_read(session, page):
        redirect('/')
    html_text = render(page.last_version().text())
    suser = getattr(session, "user", None)
    _ = get_underline(session, request)
    return dict(_=_, page=page, html_text=html_text, suser=suser)

@route('/p/<name>/<version:int>')
@view('page')
def show_page(name, version):
    session = get_session()
    page = Page.get_or_none(Page.name == name)
    if not can_read(session, page):
        redirect('/')
    versions = page.versions
    if version > len(versions):
        redirect('/p/{}'.format(name))
    html_text = render(versions[version-1].text())
    suser = getattr(session, "user", None)
    _ = get_underline(session, request)
    return dict(_=_, page=page, html_text=html_text, suser=suser)

@route('/src/<name>')
def show_page_source(name):
    session = get_session()
    page = Page.get_or_none(Page.name == name)
    if not can_read(session, page):
        redirect('/')
    response.content_type = "text/plain"
    return page.last_version().text()

@route('/src/<name>/<version:int>')
def show_page_source(name):
    session = get_session()
    page = Page.get_or_none(Page.name == name)
    if not can_read(session, page):
        redirect('/')
    versions = page.versions
    if version > len(versions):
        redirect('/src/{}'.format(name))
    response.content_type = "text/plain"
    return versions[version-1].text()

@route('/diff/<name>/<version:int>')
@view('diff')
def show_diff(name, version):
    session = get_session()
    page = Page.get_or_none(Page.name == name)
    if not can_read(session, page):
        redirect('/')
    versions = page.versions
    if version > len(versions):
        redirect('/log/{}'.format(name))
    version = versions[version-1]
    html_table = version.html_diff()
    suser = getattr(session, "user", None)
    _ = get_underline(session, request)
    return dict(_=_, version=version, html_table=html_table, suser=suser)

@route('/log/<name>')
@view('log')
def show_log(name):
    session = get_session()
    page = Page.get_or_none(Page.name == name)
    if not can_read(session, page):
        redirect('/')
    versions = page.versions.order_by(Version.num.desc())
    suser = getattr(session, "user", None)
    _ = get_underline(session, request)
    return dict(_=_, page=page, versions=versions, suser=suser)

@route('/new')
@view('edit')
def new():
    session = get_session()
    if not can_write(session):
        redirect('/')
    _ = get_underline(session, request)
    return dict(_=_, page=None, text="", suser=session.user)

@route('/edit/<name>')
@view('edit')
def edit(name):
    session = get_session()
    if not can_write(session):
        redirect('/p/{}'.format(name))
    page = Page.get(Page.name == name)
    text = page.last_version().text()
    _ = get_underline(session, request)
    return dict(_=_, page=page, text=text, suser=session.user)

@route('/new', method='POST')
def post_new():
    session = get_session()
    if not can_write(session):
        redirect('/')
    keys = "name title text private".split()
    args = [getattr(request.forms, key) for key in keys] + [session.user]
    version = new_page(*args)
    redirect('/p/{}'.format(version.page.name))

@route('/upd/<_id:int>', method='POST')
def post_upd(_id):
    session = get_session()
    if not can_write(session):
        redirect('/')
    page = Page.get_by_id(_id)
    page.title = request.forms.title
    page.save()
    text = request.forms.text
    msg = request.forms.message
    if msg:     # create new version
        version = page.new_version(text, msg, session.user)
    else:       # don't create new version
        version = page.upd_version(text)
    redirect('/p/{}'.format(version.page.name))

run(host='localhost', port=8080)
