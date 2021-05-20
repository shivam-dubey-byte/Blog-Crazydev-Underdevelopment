from flask import Flask, render_template, session, redirect, request, json
from flask_hashing import Hashing
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
import json

with open('config.json','r') as c:
    params = json.load(c)['params']

local_server = True
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.secret_key = 'key'
db = SQLAlchemy(app)
hashing = Hashing(app)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if (local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['pro_uri']

db = SQLAlchemy(app)


class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=False, nullable=False)
    title = db.Column(db.String(120),unique=False,nullable=False)
    content = db.Column(db.String(),unique=False,nullable=False)
    img = db.Column(db.VARCHAR(22),unique=True,nullable=False)
    date_time = db.Column(db.String(15),unique=False,nullable=False)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),unique=False,nullable=False)
    email = db.Column(db.VARCHAR(50),unique=True,nullable=False)
    img = db.Column(db.VARCHAR(22),unique=True,nullable=True)
    password = db.Column(db.VARCHAR(50),unique=True,nullable=False)
    date_time = db.Column(db.String(6),unique=False,nullable=False)

def verify_email(em):
    try:

        valid = validate_email(em)

        return True
    except EmailNotValidError as e:

        return False


@app.route("/")
def index():
    return render_template('index.html',message='Welcome')
@app.route("/gallery")
def _gallery_():
    return render_template('pages/gallery.html')
@app.route("/full-width")
def _full_width_():
    return render_template('pages/full-width.html')
@app.route("/sidebar-left")
def _sidebar_left_():
    return render_template('pages/sidebar-left.html')
@app.route("/sidebar-right")
def _sidebar_right_():
    return render_template('pages/sidebar-right.html')
@app.route("/basic-grid")
def _basic_grid_():
    return render_template('pages/basic-grid.html')
@app.route("/font-icons")
def _font_icons_():
    return render_template('pages/font-icons.html',form_submit='/sign-up')
@app.route('/.well-known/pki-validation/E5459302673D53989275A6261CBA42EF.txt')
def content():
		return render_template('E5459302673D53989275A6261CBA42EF.txt')
@app.route('/.well-known/pki-validation/')
def content1():
    return redirect('/.well-known/pki-validation/E5459302673D53989275A6261CBA42EF.txt')

@app.route('/sign-up',methods= ['GET','POST'])
def _sign_up_():
    if request.method=='POST':
        name = request.form.get('full-name')
        email = request.form.get('your-email')
        password = request.form.get('password')
        confirm_password = request.form.get('comfirm-password')
        date = datetime.now()
        try:
            valid = validate_email(email)
            e_mail = valid.email
            if validate_email(email) :
                if not(Users.query.filter_by(email=email).first()):
                    if password == confirm_password:
                        pass_word_key = password
                        password = hashing.hash_value(pass_word_key, salt='sha256')
                        entry = Users(name=name, email=e_mail, password=password, date_time=date)
                        db.session.add(entry)
                        db.session.commit()
                        return render_template('index.html', message='SUCCESSFUL SIGN-UP')
                    else:
                        return redirect('/sign-up')
                else:
                    return render_template('Sign-Up.html',message='email_already_exist')
            else:
                return redirect('/sign-up')
        except EmailNotValidError as e:
            return redirect('/sign-up')

    else:
        return render_template('Sign-Up.html',message='Sign-up Here')



@app.route('/log-in',methods= ['GET','POST'])
def _sign_in_():
    if 'user' not in session:
        if request.method == 'POST':

            email = request.form.get('your-email')

            password = request.form.get('password')

            validation = verify_email(email)

            if (validation and Users.query.filter_by(email=email).first()):

                data_user = Users.query.filter_by(email=email).first()
                if data_user:

                    if hashing.check_value(data_user.password, password, salt='sha256'):

                        session['user'] = data_user.id

                        return render_template('index.html',message='Login SUCCESSFUL')
                    else:
                        return render_template('log-in.html', form_submit='/log-in',
                                               error='PASSWORD_OR_EMAIL_NOT_CORRECT')
                else:
                    return render_template('log-in.html', form_submit='/log-in', error='PASSWORD_OR_EMAIL_NOT_CORRECT')

            else:
                return render_template('log-in.html', form_submit='/log-in', error='PASSWORD_OR_EMAIL_NOT_CORRECT')

        else:
            return render_template('log-in.html', form_submit='/log-in', error='')
    else:
        return render_template('index.html',message='Already Loged-in')


@app.route('/logout')
def log_out():
    if 'user' in session:
        if session['user']:
            session.pop('user')
            return render_template('index.html',message='You Logout')
    else:
        return render_template('index.html',message='Already Logout')
        


