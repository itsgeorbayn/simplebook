from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from flask_login import login_user, login_required, logout_user, current_user, AnonymousUserMixin
from app.forms import LoginForm, RegisterForm
from app.models import User
from app.extensions import db, login_manager
from app.utils import to_sentence_case, is_email_or_username

index_bp = Blueprint('index', __name__, url_prefix='/')

@index_bp.before_request
def check_login():
    if request.endpoint in ['index.index_page'] and current_user.is_authenticated:
        flash("You have already logged in!", 'warning')
        return redirect(url_for('profile.profile'))

@index_bp.route('/')
def index_page():
    return render_template('index.html')