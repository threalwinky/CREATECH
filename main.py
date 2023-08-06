# Import Libraries
from flask import *
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import *
from dotenv import load_dotenv
from datetime import timedelta
import json
import os
import shutil
import string
import random
from werkzeug.utils import secure_filename
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from hashlib import sha256
from pprint import pprint
from unidecode import unidecode
load_dotenv()

# Create app
app = Flask(__name__)
app.config['SECRET_KEY'] = "2b3ifbf302f9nc1j2po1jewkajsd"
app.config['UPLOAD_FOLDER'] = 'static/photo_url/Users'
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
GOOGLE_CLIENT_ID = "718106880185-vg443k204bnpn8u61fvmlu534dseq11b.apps.googleusercontent.com"
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")
app.permanent_session_lifetime = timedelta(minutes=50)
mail = Mail(app)
db = SQLAlchemy()
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origin="*")
# Google login
hash = {}

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback",
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)
        else:
            return function()
    return wrapper

# Database model


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    chat = db.Column(db.String)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String)
    name = db.Column(db.String)
    password = db.Column(db.String)
    photo_url = db.Column(db.String)
    color = db.Column(db.String)
    participants = db.Column(db.String)
    description = db.Column(db.String)
    chat = db.Column(db.String)
    top = db.Column(db.String)

    def __init__(self, name, participants, password, color, description):
        self.name = name
        self.password = password
        self.host = participants
        self.participants = participants
        self.photo_url = 'admin.jpg'
        self.chat = ''
        self.color = color
        self.description = description
        self.top = '1^^^^0^^^^admin.jpg^^^^-$$$$1^^^^0^^^^admin.jpg^^^^-$$$$1^^^^0^^^^admin.jpg^^^^-'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    photo_url = db.Column(db.String)
    email = db.Column(db.String)
    note = db.Column(db.String)
    # chat = db.Column(db.String, nullable=True)
    room = db.Column(db.String)

    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name
        self.photo_url = 'admin.jpg'
        # self.chat = ''
        self.room = ''
        self.note = ''

# Trailing slash


@app.route('/', methods=["POST", "GET"])
def log_in():
    found_user = User.query.filter_by(username='-').first()
    if (found_user == None):
        new_user = User('-', '123', '-')
        db.session.add(new_user)
        db.session.commit()
    if request.method == "POST":
        username = request.form['username']
        username = username.strip()
        password = request.form['password']
        # password = password.strip()
        found_user = User.query.filter_by(username=username).first()
        if username == '' or password == '':
            flash('Please enter valid username and password', 'info')
            return redirect(url_for('log_in'))
        if found_user == None:
            flash('Username not found', 'info')
            return redirect(url_for('log_in'))
        if found_user.password != password:
            flash('Wrong password', 'info')
            return redirect(url_for('log_in'))
        if found_user.email == None:
            flash("Email not activated please check your email", "info")
            return redirect(url_for("log_in"))
        session["username"] = username
        return redirect(url_for('dashboard'))
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template('log_in.html', session=session)


@app.route("/loginbygoogleaccount")
def loginbygoogleaccount():
    authorization_url, state = flow.authorization_url()
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    username = id_info["sub"]
    password = ''.join(random.choice(
        string.ascii_letters + string.digits) for _ in range(10))
    found_user = User.query.filter_by(username=username).first()
    name = id_info["name"]
    if found_user == None:
        user = User(username, password, name)
        user.email = id_info["email"]
        img_data = requests.get(id_info["picture"][:-2] + "0").content

        with open('static/photo_url/Users/' + username + '.jpg', 'wb') as handler:
            handler.write(img_data)

        db.session.add(user)
        db.session.commit()

    found_user = User.query.filter_by(username=username).first()
    found_user.photo_url = username + ".jpg"
    db.session.commit()
    return render_template('log_in_by_google_account.html', username=username, password=found_user.password)


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if (request.method == "POST"):
        username = request.form["username"]
        username = username.strip()
        password = request.form["password"]
        rpassword = request.form["rpassword"]
        email = request.form["email"]
        if username == '' or password == '':
            flash('Please enter valid username and password', 'info')
            return redirect(url_for('signup'))
        if (password != rpassword):
            flash("Password doesn't match", "info")
            return redirect(url_for("signup"))
        found_user = User.query.filter_by(username=username).first()
        user = User(username, password, username)
        if (found_user == None):
            db.session.add(user)
            db.session.commit()
        else:
            flash("The username have been taken", "info")
            return redirect(url_for("signup"))
        # notification = ["Account created! Please log in again", 1]
        # flash(notification)
        # return redirect(url_for("login"))
        sender = "noreply@app.com"
        msg_title = "Createen: Confirm your email address"
        msg = Message(msg_title, sender=sender, recipients=[email])
        hashemail = sha256(email.encode('utf-8')).hexdigest()
        hash[hashemail] = email
        msg.body = 'Hello ' + username + """,\nThanks for signing up for Createen!\nPlease click this link to confirm your email address.
This means you will be able to reset your password if you forget it later, which is especially important if you have a paid account!
If you can't click the link from your email program, please copy this URL and paste it into your web browser:
http://127.0.0.1:5000/confirmEmailSuccess/""" + username+"/" + hashemail + """ 
If you don't want to use Createen, just ignore this message and we won't bother you again.\nCheers,\nThe Create team"""
        data = {
            'username': username,
            'password': password,
            'email': email
        }
        try:
            mail.send(msg)
            return render_template('confirm_email.html', data=data)
        except Exception as e:
            print(e)
            return "The email was not sent"
    return render_template('signup.html')


@app.route('/resendEmail', methods=["POST", "GET"])
def resendEmail():
    return render_template('confirm_email.html')


@app.route('/test')
def test():
    return render_template('confirm_email.html')


@app.route('/confirmEmailSuccess/<username>/<email>', methods=["POST", "GET"])
def confirm_email(username, email):
    found_user = User.query.filter_by(username=username).first()
    email = hash[email]
    found_user.email = email
    db.session.commit()
    notification = ["Account created! Please log in again", 1]
    flash(notification)
    return redirect(url_for("log_in"))


@app.route('/log_out')
def log_out():
    session.pop("username", None)
    return redirect(url_for('log_in'))


@app.route('/dashboard')
def dashboard():
    if "username" in session:
        username = session["username"]
        found_user = User.query.filter_by(username=username).first()
        name = found_user.name
        photo_url = found_user.photo_url
        email = found_user.email
        return render_template('dashboard.html', username=username, name=name, photo_url=photo_url, email=email)
    else:
        return redirect(url_for("log_in"))

# Room Handling


@app.route('/create_room', methods=["POST", "GET"])
def create_room():
    username = session["username"]
    if (request.method == "POST"):
        room_name = request.form["room_name"]
        room_color = request.form["room_color"]
        room_description = request.form["room_description"]
        found_user = User.query.filter_by(username=username).first()
        random_room_password = ''.join(random.choice(
            string.ascii_letters + string.digits) for _ in range(10))
        room = Room(room_name, found_user.id, random_room_password,
                    room_color, room_description)
        db.session.add(room)
        db.session.commit()
        room_id = str(room.id)
        if (found_user.room == ''):
            found_user.room = room_id
        else:
            found_user.room = found_user.room + "####" + room_id
        db.session.commit()
        return redirect(url_for('join_room'))
    found_user = User.query.filter_by(username=username).first()
    return render_template('create_room.html', photo_url=found_user.photo_url, name=found_user.name)


@app.route('/join_room', methods=["POST", "GET"])
def join_room():
    username = session["username"]
    found_user = User.query.filter_by(username=username).first()
    all_rooms = found_user.room.split("####")
    all_rooms_attribute = []
    for room in all_rooms:
        all_rooms_attribute.append(Room.query.filter_by(id=room).first())
    if all_rooms[0] == '':
        return render_template('join_room.html', all_rooms_attribute=all_rooms_attribute[1:-1], photo_url=found_user.photo_url, name=found_user.name)
    return render_template('join_room.html', all_rooms_attribute=all_rooms_attribute, photo_url=found_user.photo_url, name=found_user.name)


@app.route('/remove_room', methods=["POST", "GET"])
def remove_room():
    username = session["username"]
    if request.method == "POST":
        remove_room_id = request.form["remove_room_id"]
        found_user = User.query.filter_by(username=username).first()
        found_room = Room.query.filter_by(id=remove_room_id).first()
        tmp = found_user.room.split("####")
        found_user.room = ''
        for i in range(0, len(tmp)):
            if tmp[i] != remove_room_id:
                if found_user.room == '':
                    found_user.room = found_user.room + tmp[i]
                else:
                    found_user.room = found_user.room + "####" + tmp[i]
        tmp = found_room.participants.split("####")
        found_room.participants = ''
        # print(found_user.id)
        for i in range(0, len(tmp)):

            if tmp[i] != str(found_user.id):
                if found_room.participants == '':
                    found_room.participants = found_room.participants + tmp[i]
                else:
                    found_room.participants = found_room.participants + \
                        "####" + tmp[i]
        # print(found_room.participants)
        # print(found_user.room)
        db.session.commit()
    return "Remove Complete"


@app.route('/add_room/', methods=["POST", "GET"])
def add_room():
    username = session["username"]
    if request.method == "POST":
        add_room_id = request.form["add_room_id"]
        add_room_password = request.form["add_room_password"]
        add_room_link = request.form["add_room_link"]
        if add_room_link != '':
            tmp = add_room_link.split(
                "http://127.0.0.1:5000/add_room/")[1].split("/")
            add_room_id = tmp[0]
            add_room_password = tmp[1]
        found_user = User.query.filter_by(username=username).first()
        found_room = Room.query.filter_by(id=add_room_id).first()
        if found_room == None:
            flash("Room ID not found")
            return redirect(url_for('add_room'))
        if found_room.password != add_room_password:
            flash("Room password doesn't match")
            return redirect(url_for('add_room'))
        if str(found_user.id) in found_room.participants.split("####"):
            flash("You've joined this room")
            return redirect(url_for('add_room'))
        found_room.participants = found_room.participants + \
            "####" + str(found_user.id)
        if found_user.room == '':
            found_user.room = add_room_id
        else:
            found_user.room = found_user.room + "####" + add_room_id
        db.session.commit()
    return "Add Complete"


@socketio.on('message')
def handle_message(message):
    print(message)
    msg = message.split("$$$$")
    if msg[0] == 'challenge':

        send(msg, broadcast=True)
    else:
        found_room = Room.query.filter_by(id=msg[0]).first()
        found_room.chat += "####" + msg[1] + "^^^^" + msg[2]
        db.session.commit()
        send(msg, broadcast=True)


@app.route('/useRoom/<room_id>', methods=["POST", "GET"])
def use_room(room_id):
    username = session["username"]
    found_user = User.query.filter_by(username=username).first()
    if room_id not in found_user.room.split("####"):
        flash("You haven't joined this room")
        return redirect(url_for('join_room'))
    found_room = Room.query.filter_by(id=room_id).first()
    found_room.participants = found_room.participants.split("####")
    room_link = "http://127.0.0.1:5000/add_room/" + \
        str(found_room.id) + "/" + found_room.password
    ranking = found_room.top
    ranking = ranking.split('$$$$')
    ranking_real = []

    def myFunc(e):
        return -int(e[1])
    for i in ranking:
        tmp = i.split('^^^^')
        ranking_real.append([tmp[0], tmp[1], tmp[2], tmp[3]])
        ranking_real.sort(key=myFunc)


    return render_template('room.html', data=found_room, photo_url=found_user.photo_url, room_link=room_link, user_id=str(found_user.id), 
                           chat=found_room.chat.split("####"), name=found_user.name, ranking=ranking_real)


@app.route('/challenge/<room_id>', methods=["POST", "GET"])
def challenge(room_id):
    username = session["username"]
    found_user = User.query.filter_by(username=username).first()
    found_room = Room.query.filter_by(id=room_id).first()
    with open('challenge_question.json') as json_file:
        question = json.load(json_file)
    print(type(question))
    return render_template('challenge.html', photo_url=found_user.photo_url, name=found_user.name, question=question, data=found_room)


@app.route('/change_answer', methods=["POST", "GET"])
def change():
    if request.method == "POST":
        answer = request.form["answer"]
        return unidecode(answer).lower()
    return answer


@app.route('/res', methods=["POST", "GET"])
def res():
    if request.method == "POST":
        score = request.form["score"]
        name = request.form["name"]
        found_user = User.query.filter_by(name=name).first()
        room = request.form["room"]
        found_room = Room.query.filter_by(id=room).first()
        found_room.top = found_room.top + "$$$$" + \
            str(found_user.id) + "^^^^" + str(score) + "^^^^" + found_user.photo_url + "^^^^" + found_user.name
        db.session.commit()
    return "123"


@app.route("/individual_room")
def individual_room():
    return render_template("individual_room.html")


@app.route("/users")
def users():
    user_list = db.session.execute(
        db.select(User).order_by(User.username)).scalars()
    return render_template("listUsers.html", users=user_list)


@app.route("/rooms")
def rooms():
    user_list = db.session.execute(
        db.select(Room).order_by(Room.name)).scalars()
    return render_template("listRooms.html", users=user_list)

# Setting up


@app.route('/setting_up', methods=["POST", "GET"])
def setting_up():
    username = session["username"]
    found_user = User.query.filter_by(username=username).first()
    if request.method == "POST":
        name = request.form["name"]

        avatar = request.files["new-avatar"]
        filename = avatar.filename
        arr = ["png", "jpg", "jpeg", "gif", "svg"]
        if (filename != ''):
            # flash("Không có ảnh nào được gửi lên")
            # return redirect(url_for("setting_up"))
            if (filename.split('.')[1] not in arr):
                flash("File phải là hình ảnh có đuôi png, jpg, jpeg, gif, svg")
                return redirect(url_for("setting_up"))
            else:
                filename = secure_filename(avatar.filename)
                filename = username + '.' + avatar.filename.rsplit('.')[1]
                avatar.save(os.path.join(
                    current_app.config.get('UPLOAD_FOLDER'), filename))
                found_user.photo_url = filename

        found_user.name = name
        db.session.commit()
    return render_template('setting_up.html', photo_url=found_user.photo_url, username=username, name=found_user.name, email=found_user.email)


@app.route("/delete_user/<username>")
def delete_user(username):
    found_user = User.query.filter_by(username=username).first()
    session.pop("username", None)
    db.session.delete(found_user)
    db.session.commit()
    return redirect(url_for("log_in"))


# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    # socketio.run(app, debug=True, host="192.168.1.104", port=5000)
    socketio.run(app, debug=True)
