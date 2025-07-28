from flask_login import login_user, login_required, logout_user, current_user, AnonymousUserMixin
from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request, session, jsonify
from app.utils import to_sentence_case, is_email_or_username, check_verify_status, require_not_banned
from app.models import User, Message, Friendship
from app.extensions import db, login_manager
from app.forms import MessengerForm
from sqlalchemy import or_, and_
from datetime import datetime
import os

messages_handler_bp = Blueprint('messages', __name__, url_prefix='/messages')

@messages_handler_bp.route('/send_message', methods=['POST'])
@login_required
@require_not_banned
def send_message():
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    form = MessengerForm()
    
    content = form.content.data
    friend_id = request.args.get('friend_id')
    
    message = Message(sender=current_user.id, receiver=friend_id, sended_at=datetime.now(), content=content)
    
    db.session.add(message)
    db.session.commit()
    
    message.send_news()
    return redirect(url_for('friends.friends_profile', friend_id=friend_id))

@messages_handler_bp.route('/<action>/<int:id>', methods=['GET'])
@login_required
@require_not_banned
def handle_message_action(action, id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    message = db.session.query(Message).filter_by(id=id).first()
    if message:
        friend_id=request.args.get('friend_id')
        match action:
            case 'edit':
                return redirect(url_for('messages.edit_message', id=id, friend_id=friend_id))
            case 'forward':
                return redirect(url_for('messages.forward_message', id=id, friend_id=friend_id))
            case 'remove':
                message.is_deleted = True
                message.deleted_at = datetime.now()
                
                db.session.commit()
    return redirect(url_for('friends.friends_profile', friend_id=friend_id))

@messages_handler_bp.route('edit/<id>', methods=['GET'])
@login_required
@require_not_banned
def edit_message(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    message = db.session.get(Message, id)
    if message:
        form = MessengerForm()
        
        return render_template('edit_message.html', form=form, id=id, content=message.content)

@messages_handler_bp.route('edit/<id>', methods=['POST'])
@login_required
@require_not_banned
def edit_message_submit(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    form = MessengerForm()

    message = db.session.get(Message, id)
    if message and message.sender == current_user.id and message.is_deleted == False:
        message.content = form.content.data
        message.tag_as_edited()
        db.session.commit()
        
        flash("Successfully edited", 'success')
    else:
        flash("Can't edit this message", 'error')
    if 'last_profile_friend_id' in session:
        return redirect(url_for('friends.friends_profile', friend_id=session['last_profile_friend_id']))
    else:
        return redirect(url_for('profile.profile'))

@messages_handler_bp.route('/forward/<id>', methods=['GET'])
@login_required
@require_not_banned
def forward_message_form(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    friend_list = db.session.query(User, Friendship.is_accepted, Friendship.user2_id).filter(or_(and_(Friendship.user2_id == current_user.id, User.id == Friendship.user1_id), and_(Friendship.user1_id == current_user.id, User.id == Friendship.user2_id))).all()
    updated_friend_list = []
    for friend in friend_list:
        updated_friend_list.append(dict(friend[0].to_dict(), is_accepted=friend[1]))
    
    return render_template('forward.html', supabase_url=os.environ.get("SUPABASE_URL"), id=id, friends=updated_friend_list)

@messages_handler_bp.route('/forward/<id>', methods=['POST'])
@login_required
@require_not_banned
def forward_message(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    friend = db.session.query(User).filter_by(id=request.args.get('friend_id')).first()
    if friend.id == current_user.id:
        flash("Don\'t try to forward to yourself!", 'error')
        return redirect(url_for('profile.profile'))
    
    if friend:
        friendship = db.session.query(Friendship).filter((Friendship.user1_id == friend.id) | (Friendship.user2_id == friend.id)).filter((Friendship.user1_id == current_user.id) | (Friendship.user2_id == current_user.id)).first()
        
        if friendship:
            forwarding_message = db.session.query(Message).filter_by(id=id).first()
            message = Message(sender=current_user.id, receiver=friend.id, sended_at=datetime.now(), content=forwarding_message.content)
            reference = forwarding_message.reference if forwarding_message.is_forwarded else forwarding_message.id
            message.tag_as_forwarded(reference)
            db.session.add(message)
            db.session.commit()
            
            flash("Successfully forwarded", 'success')
            return redirect(url_for('friends.friends_profile', friend_id=friend.id))
        flash("Can't find this friend, try again later", 'error')
        return redirect(url_for('profile.profile'))
    flash("Can't find this user, try again later", 'error')
    return redirect(url_for('profile.profile'))

@messages_handler_bp.route('/live', methods=['GET'])
@login_required
def live_messages():
    friend_id = request.args.get('friend_id', type=int)
    after_id = request.args.get('after_id', type=int, default=0)

    messages = db.session.query(Message)\
        .filter((Message.sender == friend_id) | (Message.receiver == friend_id))\
        .filter((Message.sender == current_user.id) | (Message.receiver == current_user.id))\
        .filter(Message.id > after_id)\
        .filter_by(is_deleted=False)\
        .order_by(Message.sended_at)\
        .all()

    return jsonify([message.to_dict() for message in messages])