import os
import uuid
import getpass
import hashlib
import base64
import datetime
import difflib

from peewee import *

D = datetime.date
linelist = lambda text: text.splitlines(keepends=True)

DB_PATH = "wiki.db"
db = SqliteDatabase(DB_PATH)

SESSION_MAX_AGE = datetime.timedelta(hours=10)

class BaseModel(Model):
    class Meta:
        database = db

class Lang(BaseModel):
    code = CharField(max_length=8, unique=True)
    name = CharField(max_length=32)

class Role(BaseModel):
    kind = CharField(max_length=8, unique=True)
    desc = CharField(max_length=32)

class User(BaseModel):
    username = CharField(max_length=32, unique=True)
    realname = CharField(max_length=128)
    passhash = CharField(max_length=64)
    passsalt = CharField(max_length=64)
    role = ForeignKeyField(Role, backref="users")
    lang = ForeignKeyField(Lang, backref="users")

    def test_password(self, password):
        b_password = password.encode()
        b_pw_salt = base64.b64decode(self.passsalt)
        dk = hashlib.pbkdf2_hmac('sha256', b_password, b_pw_salt, 100000)
        pw_hash = dk.hex()
        return pw_hash == self.passhash


class Session(BaseModel):
    key = UUIDField(unique=True)
    user = ForeignKeyField(User, backref="sessions")
    start = DateTimeField()

class Page(BaseModel):
    name = CharField(max_length=32, unique=True)
    title = CharField(max_length=128)
    private = BooleanField()

    def new_version(self, text, msg, author):
        last = self.last_version()
        num = last.num + 1
        last_text = list(difflib.restore(linelist(last.diff), 2))
        diff = "".join(difflib.ndiff(last_text, linelist(text)))
        return Version.create(page=self, num=num, date=D.today(), msg=msg, diff=diff, author=author)

    # change text without creating a new version
    def upd_version(self, text):
        last = self.last_version()
        before_last_text = list(difflib.restore(linelist(last.diff), 1))
        diff = "".join(difflib.ndiff(before_last_text, linelist(text)))
        last.diff = diff
        last.save()
        return last

    def last_version(self):
        return self.versions.order_by(Version.num.desc()).first()

    def revert(self, version, author):
        msg = "Reverted to version {}".format(version.num)
        text = "".join(difflib.restore(linelist(version.diff), 2))
        return self.new_version(text, msg, author)

class Version(BaseModel):
    page = ForeignKeyField(Page, backref="versions")
    num = IntegerField()
    date = DateField()
    msg = CharField(max_length=128)
    diff = TextField()
    author = ForeignKeyField(User, backref="versions")

    def text(self):
        return "".join(difflib.restore(linelist(self.diff), 2))

    def html_diff(self):
        fromlines = difflib.restore(linelist(self.diff), 1)
        tolines   = difflib.restore(linelist(self.diff), 2)
        link = "/p/{}".format(self.page.name)
        fromdesc = "{}/{}".format(link, self.num-1)
        todesc   = "{}/{}".format(link, self.num)
        html = difflib.HtmlDiff()
        return html.make_table(fromlines, tolines, fromdesc, todesc, context=True, numlines=3)

def is_foreign_key(field):
    return isinstance(field, ForeignKeyField)

def hash_password(password):
    b_password = password.encode()
    b_pw_salt = os.urandom(32)
    dk = hashlib.pbkdf2_hmac('sha256', b_password, b_pw_salt, 100000)
    pw_hash = dk.hex()
    pw_salt = base64.b64encode(b_pw_salt).decode()  # convert binary to str()
    return pw_hash, pw_salt

def new_user(username, realname, password, role, lang):
    pw_hash, pw_salt = hash_password(password)
    return User.create(
        username=username,
        realname=realname,
        passhash=pw_hash,
        passsalt=pw_salt,
        role=role,
        lang=lang
    )

def clean_old_sessions():
    now = datetime.datetime.now()
    for session in Session.select():
        if (now - session.start) > SESSION_MAX_AGE:
            session.delete_instance()

def login(username, password):
    user = User.get_or_none(User.username == username)
    if user is None:
        return None
    if not user.test_password(password):
        return None
    clean_old_sessions()
    key = str(uuid.uuid4())
    return Session.create(key=key, user=user, start=datetime.datetime.now())

def new_page(name, title, text, private, author):
    msg = "First version"
    diff = "".join(difflib.ndiff(["\n"], linelist(text)))
    page = Page.create(name=name, title=title, private=private)
    return Version.create(page=page, num=1, date=D.today(), msg=msg, diff=diff, author=author)

all_tables = [Lang, Role, User, Session, Page, Version]

def create_tables():
    db.create_tables(all_tables)

def init_users():
    en = Lang.create(code="en", name="English")
    pt = Lang.create(code="pt", name="Português")
    reader = Role.create(kind="reader", desc="Reader")
    writer = Role.create(kind="writer", desc="Writer")
    admin  = Role.create(kind="admin", desc="Administrator")
    password = getpass.getpass("Admin Password: ")
    root = new_user("admin", "Admin", password, admin, en)

if __name__ == "__main__":
    os.remove(DB_PATH)
    create_tables()
    init_users()
