from flask import Blueprint, render_template, redirect, url_for, flash, current_app, jsonify, request, session
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import InviteFriendForm, UpdateForm, MessengerForm
from app.models import User, Friendship, Message, NewsItem
from app.extensions import db, login_manager
from app.utils import to_sentence_case, is_email_or_username, flatten, check_verify_status, require_not_banned, bool_conv
from sqlalchemy import or_, and_
from datetime import datetime
from wtforms.validators import DataRequired
import os, uuid

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/', methods=['GET'])
@login_required
def profile():
    friend_list = db.session.query(User, Friendship.is_accepted, Friendship.user2_id).filter(or_(and_(Friendship.user2_id == current_user.id, User.id == Friendship.user1_id), and_(Friendship.user1_id == current_user.id, User.id == Friendship.user2_id))).all()
    session.setdefault('show_hidden_posts', True)
    
    updated_friend_list = []
    friend_invites = []
    for friend in friend_list:
        updated_friend_list.append(dict(friend[0].to_dict(), is_accepted=friend[1]))
        if not updated_friend_list[-1]['is_accepted'] and friend[2] == current_user.id:
            friend_invites.append(updated_friend_list[-1])
            
    params = {
        "friends": updated_friend_list,
        "invites": friend_invites
    }
    
    data = current_user.to_dict()
    user_posts = current_user.get_posts(get_comments=True, get_deleted_posts=True)
    visible_posts = [post for post in user_posts if (post['is_deleted'] and session['show_hidden_posts']) or not post['is_deleted']]
                     
    return render_template('profile.html', prefix="Your", self_profile=True, visible_posts=visible_posts, user_posts=user_posts, **data, **params, body_class='profile', current_user=current_user, show_hidden_posts=session['show_hidden_posts'])

@profile_bp.route('/hidden_posts_statement/<show_hidden_posts>')
@login_required
def hidden_posts_statement(show_hidden_posts):
    show_hidden_posts = bool_conv(show_hidden_posts)
    session['show_hidden_posts'] = show_hidden_posts
    
    return redirect(url_for('profile.profile'))

@profile_bp.route('/update/<field>', methods=['GET'])
@login_required
@require_not_banned
def update_form(field):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    field_to_update = ""
    form = UpdateForm()
    match field:
        case "username":
            field_to_update = 'username'
        case "picture":
            field_to_update = 'picture'
    
    return render_template('update.html', field=field_to_update, form=form)
        
@profile_bp.route('/update/<field>', methods=['POST'])
@login_required
@require_not_banned
def update_submit(field):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    form = UpdateForm(field=field)
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            match field:
                case "username":
                    username = form.username.data
                    if db.session.query(User).filter_by(username=username).first():
                        flash("Username already exists", 'error')
                        return redirect(url_for('profile.update_form', field=field))
                    current_user.username = username
                case "picture":
                    filename = uuid.uuid4().hex[:16] + os.path.splitext(form.picture.data.filename)[1]
                    value = form.picture.data
                    if current_user.picture != "default.png":
                        os.remove(f'app/static/images/profile/{current_user.picture}')
                    form.picture.data.save(f'app/static/images/profile/{filename}')
                case default:
                    flash("Can\'t find this field", 'error')
                    return redirect(url_for('profile'))
            db.session.commit()
            flash("Successfully updated", 'success')
            return redirect(url_for('profile.profile'))
        flash("Wrong password", 'error')
        return redirect(url_for('profile.update_form', field=field))
    errors = form.errors
    for error_keys in errors:
        for error in errors[error_keys]:
            flash(f"\'{error_keys}\': {error}", 'error')
    return redirect(url_for('profile.update_form', field=field))

@profile_bp.route('/hide_news_item/<int:id>')
@login_required
def hide_news_item(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    news_item = db.session.get(NewsItem, id)
    
    if news_item and news_item.recipient_id == current_user.id:
        db.session.delete(news_item)
        db.session.commit()
        
        flash("Successfully deleted", 'success')
    else:
        flash("Can\'t delete this news item", 'error')

    return redirect(url_for('profile.profile'))