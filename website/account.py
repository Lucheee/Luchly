from random import randint
from flask import Blueprint, redirect, render_template, url_for, request, flash
from .models import db, User
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash




account = Blueprint("account", __name__)
mail = Mail()

otp = randint(100000,999999)

@account.route('/validate/<email>', methods=['GET', 'POST'])
def validate(email):
    user = User.query.filter_by(email=email).first()
    if user:
        if request.method == 'POST':
            user_otp = request.form['otp']
            if not user_otp:
                flash('Please enter OTP.')
                return redirect(url_for('account.validate', email=email))
            if int(user_otp) == otp:
                user.confirm = True
                db.session.commit()
                flash('Email verified successfully.', category='success')
                return redirect(url_for('auth.login'))
            else:
             flash('Invalid OTP, kindly request for another otp', category='error')
             return redirect(url_for('account.validate', email=email))
        return render_template('validate.html', email=email)
    return 'Email not found.'


@account.route('/resend/<email>')
def resend(email):
    user = User.query.filter_by(email=email).first()
    if user:
        try:
            msg = Message('Email Verification', sender="oluchie51@gmail.com", recipients=[email])
            msg.html = render_template('otp.html', otp=str(otp))
            mail.send(msg)
        except:
            flash ("Verification failed. Please try again.")
            return redirect(url_for('auth.register'))
        flash('OTP sent successfully. Please check your mail inbox or spam.')
        return redirect(url_for('account.validate', email=email))
    return 'Email not found.'

@account.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email.lower()).first()
        link = request.host_url + "reset_password/" + email
        if user:
            try:
                msg = Message('Reset Password', sender="oluchie51@gmail.com", recipients=[email])
                msg.html = render_template('reset_mail.html', link=link)
                mail.send(msg)
            except:
                flash ("Reset password failed. Please try again.")
                return redirect(url_for('auth.login'))
            flash('Reset password link sent successfully. Please check your mail inbox or spam.')
            return redirect(url_for('auth.login'))
        flash('Email not found.')
        return redirect(url_for('account.forgot_password'))
    return render_template('reset.html')

@account.route('/reset_password/<email>', methods=['GET', 'POST'])
def reset_password(email):
    user = User.query.filter_by(email=email).first()
    if user:
        if request.method == 'POST':
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            if password == confirm_password:
                user.password = generate_password_hash(password, method='sha256')
                db.session.commit()
                flash('Password reset successfully. Please login.')
                return redirect(url_for('auth.login'))
            else:
                flash('Passwords do not match. Please try again.')
                return redirect(url_for('account.reset_password', email=email))
        return render_template('reset-password.html', email=email)
    return 'Email not found.'