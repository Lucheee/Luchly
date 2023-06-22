from random import randint
from flask import Blueprint, render_template, redirect, url_for, flash, request
from .models import User
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_mail import Message, Mail


bcrypt = Bcrypt()
mail = Mail()

auth = Blueprint("auth", __name__)
otp = randint(100000,999999)


@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
               # flash('Logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('urls.shorten_url'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("sign-in.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("base.home"))


@auth.route("/register", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        username_exists = User.query.filter_by(username=username).first()
        email_exists = User.query.filter_by(email=email.lower()).first()

        if username_exists:
            flash('Username already taken, choose another username.', category="error")
        elif email_exists:
            flash('Email Address already taken, choose another email address.', category="error")
        elif password != confirm_password:
            flash('Password do not match!', category='error')
        elif len(username) < 4:
            flash('Username is too short!', category='error')
        elif len(password) < 6:
            flash('Password is too short!', category='error')
        elif len(email) < 5:
            flash('Email is invalid', category='error')
        else:
              
            password = generate_password_hash(password, method='sha256')
            new_user = User(username=username,email=email.lower(), password=password)
            
            try:
                msg = Message("Luchly Email Verification", sender="oluchie51@gmail.com", recipients=[email])
                msg.html = render_template('otp.html', otp=str(otp), username=username)
                mail.send(msg)
            except Exception as e:
                print(e)
                flash ("Verification failed. Please try again.")
                return redirect(url_for('auth.signup'))

            
            new_user.save()
            flash('Account created successfully. Please check your mail inbox or spam for verification.')
            return redirect(url_for('account.validate', email=email.lower()))

            #db.session.add(new_user)
            #db.session.commit()
            #login_user(new_user, remember=True)
            #flash('User created successfully!', category="success")
           # return redirect(url_for('auth.login'))
        

    return render_template("sign-up.html", user=current_user)
