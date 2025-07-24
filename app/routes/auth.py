from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user, AnonymousUserMixin
from app.forms import LoginForm, RegisterForm, VerificationForm
from app.models import User, UserVerification
from app.extensions import db, login_manager
from app.utils import to_sentence_case, is_email_or_username, send_email
import uuid
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.before_request
def before():
    if current_user.is_authenticated and request.method == 'GET':
        if request.endpoint in ['auth.login_form', 'auth.register_form']:
            flash("You have already logged in!", 'warning')
            return redirect(url_for('profile.profile'))
        elif request.endpoint in ['auth.verification_form'] and current_user.is_verified:
            flash("You have already verified!", 'warning')
            return redirect(url_for('profile.profile'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out!', 'success')
    return redirect(url_for('index.index_page'))

@auth_bp.route('/login', methods=['GET'])
def login_form():
    params = {
        "form": LoginForm()
    }
    
    return render_template('login.html', **params)

@auth_bp.route('/login', methods=['POST'])
def login_submit():
    form = LoginForm()
    password = form.password.data
    remember = 'remember' in request.form
    
    type = is_email_or_username(form.username_or_email.data)
    params = {type: form.username_or_email.data}
    
    user = db.session.query(User).filter_by(**params).first()
    
    if user:
        if user.check_password(password):
            login_user(user, remember=remember)
            return redirect(url_for('profile.profile'))
        flash("Wrong password, try again", 'error')
    else:
        flash(f"Unknown {type}, try again", 'error')
    return redirect(url_for('auth.login_form'))

@auth_bp.route('/register', methods=['GET'])
def register_form():
    params = {
        "form": RegisterForm()
    }
    
    return render_template('register.html', **params)

@auth_bp.route('/register', methods=['POST'])
def register_submit():
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        if db.session.query(User).filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register_form'))
        
        elif db.session.query(User).filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('auth.register_form'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()
        
        login_user(user)
        new_verification(user)
        
        flash('Successfully registered. Verify your email, check code on email.', 'success')
        return redirect(url_for('auth.verification_form'))
    
    for field, messages in form.errors.items():
        for message in messages:
            flash(f"{to_sentence_case(field)}: {message}", 'error')
        
    return redirect(url_for('auth.register_form'))

@auth_bp.route('/verify', methods=['GET'])
@login_required
def verification_form():
    params = {
        "form": VerificationForm(),
    }
    
    return render_template('verification.html', **params)

@auth_bp.route('/verify', methods=['POST'])
@login_required
def verification_submit():
    form = VerificationForm()
    
    code = str(form.verification_code.data).upper()
    user_verification = db.session.query(UserVerification).filter_by(user_id=current_user.id).first()

    if not user_verification:
        flash("Can't find your verification", 'error')
        return redirect(url_for('auth.verification_form'))

    elif not user_verification.verification_code == code:
        flash("Wrong verification code", 'error')
        return redirect(url_for('auth.verification_form'))
    
    elif datetime.now() < user_verification.code_expiration:
        current_user.is_verified = True
        
        db.session.delete(user_verification)
        db.session.commit()
        flash("Succesfully verified", 'success')
        return redirect(url_for('profile.profile'))
    
    db.session.delete(user_verification)
    db.session.flush()
    
    new_verification(current_user)
    
    flash("Verification time expired, check code on email and try again", 'error')
    return redirect(url_for('auth.verification_form'))

def new_verification(user):
    user_verification = UserVerification.new(user_id=user.id)
    db.session.add(user_verification)
    db.session.flush()
    send_email(
        subject="Email Verification",
        body=f"Here it is your verification code, that will expire in one hour: {user_verification.verification_code}",
        recipient=current_user.email
    )
    db.session.commit()