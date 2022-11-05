from flask import Flask, request, render_template, send_from_directory
from forms import *
from apsw import Error
import secrets
import dbHandler
from threading import local

tls = local()

#Setting up app
app = Flask(__name__)

# The secret key enables storing encrypted session data in a cookie
app.secret_key = secrets.token_hex(64)

# Adding a login manager to the app
import flask_login
from flask_login import login_required, login_user, logout_user, current_user
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"

# Class to store user info
# UserMixin provides us with an `id` field and the necessary
# methods (`is_authenticated`, `is_active`, `is_anonymous` and `get_id()`)
class User(flask_login.UserMixin):
    pass

# This method is called whenever the login manager needs to get
# the User object for a given user id
@login_manager.user_loader
def user_loader(user_id):
    
    # For a real app, we would load the User from a database or something
    user = User()
    user.id = user_id
    return user

@app.route('/index.js')
def index_js():
    return send_from_directory(app.root_path, 'static/index.js', mimetype='text/javascript')

@app.route('/index.css')
def index_css():
    return send_from_directory(app.root_path, 'static/index.css', mimetype='text/css')

@app.route('/')
@app.route('/index.html')
@login_required
def index_html():
    return render_template("index.html", minetype='text/html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if request.method == 'GET':
        return render_template('./login.html', form=form)
        
    if request.method == 'POST': 
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            try: 
                isValid = dbHandler.check_password(username, password)
            except IndexError as e:
                return render_template('./login.html', form=form)  
            if(isValid):
                user = user_loader(username)
                
                # automatically sets logged in session cookie
                login_user(user)
        
                flask.flash('Logged in successfully.')
                next = flask.request.args.get('next')
                
                if not is_safe_url(next):
                    return flask.abort(400)

                return flask.redirect(next or flask.url_for('index_html'))              
    return render_template('./login.html', form=form)