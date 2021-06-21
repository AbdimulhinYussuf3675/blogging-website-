from . import auth
from flask import flash,render_template,redirect,url_for,request
from flask_login import login_user,logout_user,login_required
from ..models import User
from .forms import RegistrationForm,LoginForm
from .. import db
from ..email import mail_message

@auth.route('/login',methods=['GET','POST'])
def login():
    '''
    View Function to login users
    '''
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return render_template('home.html')
    flash('Invalid username or password !')
    title = "Bloggers Login"
    return render_template('auth/login.html',login_form = login_form,title = title)

@auth.route('/register',methods = ["GET","POST"])
def register():
    '''
    View Function to register new users
    '''
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You've been successfully registered!")
        mail_message("Welcome to Bloggers","email/welcome_user",user.email,user=user)
        return redirect(url_for('auth.login'))
    title = "Bloggers registration"
    return render_template('auth/register.html',registration_form = form, title = title)

@auth.route('/logout')
@login_required
def logout():
    '''
    View Function to logout a user
    '''
    logout_user()
    flash("You've been successfully registered!")
    return redirect(url_for("main.index"))
