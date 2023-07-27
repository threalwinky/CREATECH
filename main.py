#Import Libraries
from flask import *
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
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
load_dotenv()

#Create app
app = Flask(__name__)
app.config['SECRET_KEY'] = "2b3ifbf302f9nc1j2po1jewkajsd"
app.config['UPLOAD_FOLDER'] = 'static/photoUrl/Users'
app.config['MAIL_SERVER'] = "smtp.googlemail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
GOOGLE_CLIENT_ID = "718106880185-vg443k204bnpn8u61fvmlu534dseq11b.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
app.permanent_session_lifetime = timedelta(minutes=50)
mail = Mail(app)
db = SQLAlchemy()
db.init_app(app)

#Google login
hash = {}

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback",
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()
    return wrapper

#Database model
class Room(db.Model):
    room_id = db.Column(db.Integer, primary_key = True)
    room_name = db.Column(db.String)
    room_password = db.Column(db.String)
    photo_Url = db.Column(db.String)
    color = db.Column(db.String)
    participants = db.Column(db.String)
    description = db.Column(db.String)
    chat = db.Column(db.String)
    def __init__(self, room_name, participants, room_password):
        self.room_name = room_name
        self.room_password = room_password
        self.participants = participants
        self.photo_Url = 'admin.jpg'
        self.chat = ''

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    photoUrl = db.Column(db.String)
    email = db.Column(db.String)
    # chat = db.Column(db.String, nullable=True)
    room = db.Column(db.String)
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.photoUrl = 'admin.jpg'
        # self.chat = ''
        self.room = ''

#Trailing slash
@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        username = username.strip()
        password = request.form['password']
        
        found_user = User.query.filter_by(username=username).first()
        if username == '' or password == '':
            flash('Please enter valid username and password', 'info')
            return redirect(url_for('login'))
        if found_user == None:
            flash('Username not found', 'info')
            return redirect(url_for('login'))
        if found_user.password != password:
            flash('Wrong password', 'info')
            return redirect(url_for('login'))
        if found_user.email == None :
            flash("Email not activated please check your email", "info")
            return redirect(url_for("login"))
        session["username"] = username
        print(username)
        return redirect(url_for('dashboard'))
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template('login.html', session=session)

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
    token_request = google.auth.transport.requests.Request(session=cached_session)
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    username = id_info["sub"]
    password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    found_user = User.query.filter_by(username=username).first()
    if found_user == None:
        user = User(username, password)
        user.email = id_info["email"]
        img_data = requests.get(id_info["picture"][:-2] + "0").content
        print(id_info["picture"])
        with open('static/photoUrl/Users/' + username + '.jpg', 'wb') as handler:
            handler.write(img_data)
        
        db.session.add(user)
        db.session.commit()
        
        
    found_user = User.query.filter_by(username=username).first()
    found_user.photoUrl = username + ".jpg"
    db.session.commit()
    return render_template('loginbygoogleaccount.html', username=username, password=found_user.password)



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
        user = User(username, password)
        if (found_user == None):
            db.session.add(user)
            db.session.commit()
        else :
            flash("The username have been taken", "info")
            return redirect(url_for("signup"))
        # notification = ["Account created! Please log in again", 1]
        # flash(notification)
        # return redirect(url_for("login"))
        sender = "noreply@app.com"
        msg_title = "EasyLearning: Confirm your email address"
        msg = Message(msg_title, sender=sender, recipients=[email])
        hashemail = sha256(email.encode('utf-8')).hexdigest()
        hash[hashemail] = email
        msg.body = 'Hello ' + username + """,\nThanks for signing up for EasyLearning!\nPlease click this link to confirm your email address.\n
This means you will be able to reset your password if you forget it later, which is especially important if you have a paid account!
If you can't click the link from your email program, please copy this URL and paste it into your web browser:
http://127.0.0.1:5000/confirmEmailSuccess/"""+ username+"/" +hashemail+ """ 
If you don't want to use EasyLearning, just ignore this message and we won't bother you again.\nCheers,\nThe Create team"""
        data = {
            'username' : username,
            'password' : password,
            'email' : email
        }
        try:
            mail.send(msg)
            return render_template('confirmEmail.html', data=data)
        except Exception as e:
            print(e)
            return "The email was not sent"
    return render_template('signup.html')

@app.route('/confirmEmailSuccess/<username>/<email>', methods=["POST", "GET"])
def confirm_email(username, email):
    found_user = User.query.filter_by(username=username).first()
    email = hash[email]
    found_user.email = email
    db.session.commit()
    notification = ["Account created! Please log in again", 1]
    flash(notification)
    return redirect(url_for("login"))

@app.route('/logout')
def log_out():
    session.pop("username", None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if "username" in session:
        username = session["username"]
        print(session)
        return render_template('dashboard.html', username=username)
    else:
        return redirect(url_for("login"))

#Room Handling
@app.route('/createRoom', methods=["POST", "GET"])
def create_room():
    if (request.method == "POST"):
        room_name = request.form["roomname"]
        username = session["username"]
        found_user = User.query.filter_by(username=username).first()
        random_room_password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        room = Room(room_name, username, random_room_password)
        db.session.add(room)
        db.session.commit()
        room_id = str(room.room_id)
        if (found_user.room == ''):
            found_user.room = room_id
        else:
            found_user.room = found_user.room + "####" + room_id
        db.session.commit()
        return redirect(url_for('join_room'))
    return render_template('createRoom.html')

@app.route('/joinRoom', methods=["POST", "GET"])
def join_room():
    username = session["username"]
    found_user = User.query.filter_by(username=username).first()
    all_rooms = found_user.room.split("####")
    if all_rooms[0] == '':
        return render_template('joinRoom.html', all_rooms=all_rooms[1:-1])
    return render_template('joinRoom.html', all_rooms=all_rooms)

@app.route('/removeRoom', methods=["POST", "GET"])
def remove_room():
    username = session["username"]
    if request.method == "POST":
        remove_room_id = request.form["remove_room_id"]
        found_user = User.query.filter_by(username=username).first()
        found_room = Room.query.filter_by(room_id=remove_room_id).first()
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
        for i in range(0, len(tmp)):
            if tmp[i] != username:
                if found_room.participants == '':
                    found_room.participants = found_room.participants + tmp[i]
                else:
                    found_room.participants = found_room.participants + "####" + tmp[i]
        # print(found_user.room)
        
        db.session.commit()
    return "Remove Complete"

@app.route('/addRoom', methods=["POST", "GET"])
def add_room():
    username = session["username"]
    if request.method == "POST":
        add_room_id = request.form["add_room_id"]
        add_room_password = request.form["add_room_password"]
        print(username ,add_room_id)
        found_user = User.query.filter_by(username=username).first()
        found_room = Room.query.filter_by(room_id=add_room_id).first()
        if found_room == None :
            flash("Room ID not found")
            return redirect(url_for('add_room'))
        if found_room.room_password != add_room_password :
            flash("Room password doesn't match")
            return redirect(url_for('add_room'))
        if username in found_room.participants.split("####"):
            flash("You've joined this room")
            return redirect(url_for('add_room'))
        found_room.participants = found_room.participants + "####" + username
        if found_user.room == '' :
            found_user.room = add_room_id
        else :
            found_user.room = found_user.room + "####" + add_room_id
        db.session.commit()
    return "Add Complete"

@app.route('/useRoom/<room_id>', methods=["POST", "GET"])
def use_room(room_id):
    username = session["username"]
    found_user = User.query.filter_by(username=username).first()
    if room_id not in found_user.room.split("####"):
        flash("You haven't joined this room")
        return redirect(url_for('join_room'))
    print(room_id)
    found_room = Room.query.filter_by(room_id=room_id).first()
    found_room.participants = found_room.participants.split("####")
    return render_template('room.html', data=found_room)



@app.route("/individualRoom")
def individual_room():
    return render_template("individualRoom.html")

@app.route("/users")
def users():
    user_list = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("listUsers.html", users=user_list)

@app.route("/rooms")
def rooms():
    user_list = db.session.execute(db.select(Room).order_by(Room.room_name)).scalars()
    return render_template("listRooms.html", users=user_list)



#Setting up
@app.route('/settingup', methods=["POST","GET"])
def settingup():
    username = session["username"]
    found_user = User.query.filter_by(username=username).first()
    if request.method == "POST":
        avatar = request.files["new-avatar"]
        filename = avatar.filename
        arr = ["png", "jpg", "jpeg", "gif", "svg"]
        if (filename == ''):
            flash("Không có ảnh nào được gửi lên")
            return redirect(url_for("settingup"))
        if (filename.split('.')[1] not in arr):
            flash("File phải là hình ảnh có đuôi png, jpg, jpeg, gif, svg")
            return redirect(url_for("settingup"))
        else :
            filename = secure_filename(avatar.filename)
            filename = username + '.' + avatar.filename.rsplit('.')[1]
            avatar.save(os.path.join(current_app.config.get('UPLOAD_FOLDER'), filename))
            found_user.photoUrl = filename
            db.session.commit()
    return render_template('settingup.html', photoUrl=found_user.photoUrl, username=username)

@app.route("/deleteuser/<username>")
def deleteuser(username):
    found_user = User.query.filter_by(username=username).first()
    session.pop("username", None)
    db.session.delete(found_user)
    db.session.commit()
    return redirect(url_for("login"))
#Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)