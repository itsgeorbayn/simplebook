from flask import Blueprint, render_template, redirect, url_for, flash, current_app, jsonify, request, session
from app.utils import check_verify_status, require_not_banned
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User, Friendship, Post, Message, NewsItem
from app.forms import InviteFriendForm, MessengerForm
from app.extensions import db, login_manager
from sqlalchemy import or_, and_
from datetime import datetime
import os

friends_bp = Blueprint('friends', __name__, url_prefix='/friends')

@friends_bp.route('/invite', methods=['GET'])
@login_required
@require_not_banned
def invite_friend():
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    params = {
        "form": InviteFriendForm(),
    }
    return render_template('invite_friend.html', **params)

@friends_bp.route('/invite', methods=['POST'])
@login_required
@require_not_banned
def invite_friend_send():
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    form = InviteFriendForm()
    
    friend = db.session.query(User).filter_by(username=form.username.data).first()
    if friend:
        are_friends = db.session.query(Friendship).filter((Friendship.user1_id == friend.id) | (Friendship.user2_id == friend.id)).filter((Friendship.user1_id == current_user.id) | (Friendship.user2_id == current_user.id)).first()
    else:
        are_friends = False
    
    conditions = [friend, friend != current_user, not are_friends]
    
    if all(conditions):
        friendship = Friendship(user1_id=current_user.id, user2_id=friend.id, created_at=datetime.now(), is_accepted=False)
        
        db.session.add(friendship)
        db.session.commit()
        
        flash("User has been successfully invited to friends!", 'success')
        return redirect(url_for('profile.profile'))
    elif not friend:
        flash("This user doesn't exist!", 'error')
    elif friend == current_user:
        flash("You can't become your own friend :(", 'error')
    elif are_friends and not are_friends.is_accepted and are_friends.user1_id == friend.id:
        flash("This user has already sent invite to you!", 'error')
    elif are_friends and not are_friends.is_accepted and are_friends.user1_id == current_user.id:
        flash("You have already sent invite to this user!", 'error')
    elif are_friends and are_friends.is_accepted:
        flash("You are already friends with this user!", 'error')
    return redirect(url_for('friends.invite_friend'))

@friends_bp.route('/add_friend', methods=['POST'])
@login_required
@require_not_banned
def add_friend():
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    id = int(request.args.get("id"))
    friendship = db.session.query(Friendship).filter(Friendship.user1_id == id, Friendship.user2_id == current_user.id).first()
    if request.form.get("response") == "yes":
        friendship.is_accepted = True
        db.session.commit()
        
        flash("You have successfully accepted a user's invitation to friends", 'success')
        return redirect(url_for('profile.profile'))
    elif request.form.get("response") == "no":
        db.session.delete(friendship)
        db.session.commit()
        
        flash("You have successfully declined a user's invitation to friends", 'success')
        return redirect(url_for('profile.profile'))

@friends_bp.route('/profile', methods=['GET'])
@login_required
def friends_profile():
    form = MessengerForm()
    friend = db.session.query(User).filter_by(id=request.args.get('friend_id')).first()
    if friend.id == current_user.id:
        flash("Don\'t try to open yourself!", 'error')
        return redirect(url_for('profile.profile'))
        
    if friend:
        friendship = db.session.query(Friendship).filter((Friendship.user1_id == friend.id) | (Friendship.user2_id == friend.id)).filter((Friendship.user1_id == current_user.id) | (Friendship.user2_id == current_user.id)).first()
        
        if friendship:
            data = {('friend_id' if k == 'id' else k): v for k, v in friend.to_dict().items()}
            
            user_posts = friend.get_posts(get_comments=True)
            visible_posts = [post for post in user_posts if (post['is_deleted'] and session['show_hidden_posts']) or not post['is_deleted']]
        
            messages = db.session.query(Message).filter((Message.sender == friend.id) | (Message.receiver == friend.id)).filter((Message.sender == current_user.id) | (Message.receiver == current_user.id)).filter_by(is_deleted=False).order_by(Message.sended_at).all()
            messages_data = [message.to_dict() for message in messages]
            
            session['last_profile_friend_id'] = friend.id
            news_related_to_friend = db.session.query(NewsItem).filter(NewsItem.recipient_id == current_user.id).all()
            
            for item in [news_item for news_item in news_related_to_friend if news_item.reference_author.id == friend.id]:
                db.session.delete(item)
            db.session.commit()
            
            return render_template('profile.html', supabase_url=os.environ.get("SUPABASE_URL"), friend_user=friend, form=form, id=current_user.id, prefix="Friend's", friends_profile=True, visible_posts=visible_posts, user_posts=user_posts, body_class='profile', messages=messages_data, current_user_id=current_user.id, **data)
        flash("Can't find this friend, try again later", 'error')
        return redirect(url_for('profile.profile'))
    flash("Can't find this user, try again later", 'error')
    return redirect(url_for('profile.profile'))

@friends_bp.route('/remove/<id>', methods=['POST'])
@login_required
@require_not_banned
def remove_friend(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    friendship = db.session.query(Friendship).filter((Friendship.user1_id == id) | (Friendship.user2_id == id)).filter((Friendship.user1_id == current_user.id) | (Friendship.user2_id == current_user.id)).first()
    
    if friendship:
        db.session.delete(friendship)
        db.session.commit()
        
        flash("Friend deleted successfully", 'success')
        return redirect(url_for('profile.profile'))
    flash("Can\'t find this friendship", 'error')