from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user, AnonymousUserMixin
from app.forms import LoginForm, RegisterForm, VerificationForm, CreatePostForm, MessengerForm
from app.models import User, UserVerification, AdminPermission, Post, Comment, Message
from app.extensions import db, login_manager
from app.utils import to_sentence_case, check_verify_status, Symbols, translate_checkbox
from datetime import datetime, timedelta
import os, uuid

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def before():
    is_admin = db.session.get(AdminPermission, current_user.id)
    
    if not is_admin:
        flash("You are not admin!", 'error')
        return redirect(url_for('profile.profile'))
    
@admin_bp.route('/panel')
@login_required
def panel():
    admin = db.session.get(AdminPermission, current_user.id)
    
    params = []
    comments = []
    show_full_message = request.args.get('show_full_message')
    
    selected_action = request.args.get('selected_action')
    match selected_action:
        case "list_users":
            if admin.list_users:
                params = db.session.query(User).order_by(User.id).all()
                
        case "list_posts":
            if admin.list_posts:
                params = db.session.query(Post).order_by(Post.id).all()
            edit = request.args.get('edit')
            if edit and admin.list_comments:
                comments = db.session.query(Comment).filter_by(post_id=edit).order_by(Comment.id).all()
                
        case "list_admins":
            if admin.list_admins:
                params = db.session.query(AdminPermission).order_by(AdminPermission.id).all()
                
        case "list_messages":
            if admin.list_messages:
                params = db.session.query(Message).order_by(Message.id).all()
        
    return render_template('admin_panel.html', selected_action=selected_action, params=params, comments=comments, body_class='admin', admin=admin, show_full_message=show_full_message)
    

@admin_bp.route('/update/user', methods=['POST'])
@login_required
def update_user_info():
    form = request.form
    files = request.files
    
    edit = request.args.get('edit')
    user = User.query.get(edit)
    
    fields = user.find_updated_fields(form, files)
    
    for field in fields:
        if field == 'picture':
            picture = files.get('picture')
            filename = uuid.uuid4().hex[:16] + os.path.splitext(picture.filename)[1]
            if user.picture != "default.png":
                os.remove(f'app/static/images/profile/{user.picture}')
            picture.save(f'app/static/images/profile/{filename}')
            user.picture = filename
        elif field == 'username':
            username = form.get('username')
            if db.session.query(User).filter_by(username=username).first():
                flash("Username already exists", 'error')
                return redirect(url_for('profile.update_form', field=field))
            user.username = username
    db.session.commit()
    
    return redirect(url_for('admin.panel', selected_action='list_users', edit=edit))

@admin_bp.route('/update/post', methods=['POST'])
@login_required
def update_post_info():
    form = request.form
    
    edit = request.args.get('edit')
    post = Post.query.get(edit)
    
    fields = post.find_updated_fields(form)
    
    for field in fields:
        if field == 'title':
            title = form.get('title')
            post.title = title
    db.session.commit()
        
    return redirect(url_for('admin.panel', selected_action='list_posts', edit=edit))

@admin_bp.route('/update/message', methods=['POST'])
def update_message_info():
    pass

@admin_bp.route('/update/admin', methods=['POST'])
@login_required
def update_admin_info():
    form = request.form
    
    edit = request.args.get('edit')
    admin = AdminPermission.query.get(edit)
    
    fields = admin.find_updated_fields(form)
    for key in fields:
        setattr(admin, key, fields[key])
    db.session.commit()
    
    return redirect(url_for('admin.panel', selected_action='list_admins', edit=edit))


@admin_bp.route('/delete/post/<int:id>')
@login_required
def delete_post_form(id):
    post = db.session.get(Post, id)
    if post:
        post.mark_as_deleted()
        db.session.commit()
        
        flash("Post has been successfully deleted!", 'success')
    else:
        flash("Post has not found.", 'error')
    return redirect(url_for('admin.panel', selected_action='list_posts'))

@admin_bp.route('/return/post/<int:id>')
@login_required
def return_post_form(id):
    post = db.session.get(Post, id)
    if post:
        post.mark_as_returned()
        db.session.commit()
        
        flash("Post has been successfully returned!", 'success')
    else:
        flash("Post has not found.", 'error')
    return redirect(url_for('admin.panel', selected_action='list_posts'))
    
@admin_bp.route('/edit/post/<int:id>', methods=['GET'])
@login_required
def edit_post_form(id):
    admin = db.session.get(AdminPermission, current_user.id)
    
    post = db.session.get(Post, id)
    if not admin.edit_posts:
        flash("You have no rights to do it.", 'error')
    elif post:
        params = {
            "form": CreatePostForm(),
            "title": post.title,
            "content": post.content
        }
        
        return render_template('create_post.html', id=id, show_title=True, header="Edit Post as Admin", type="edit", action=url_for('admin.edit_post', id=id), **params)
    flash("This post cannot be edited!", 'error')
    return redirect(url_for('admin.panel'))

@admin_bp.route('/edit_post/<int:id>', methods=['POST'])
@login_required
def edit_post(id):
    admin = db.session.get(AdminPermission, current_user.id)
    
    post = db.session.get(Post, id)
    if not admin.edit_posts:
        flash("You have no rights to do it.", 'error')
    elif post:
        form = CreatePostForm()
        
        title = Symbols.clean_title(form.title.data)
        content = form.content.data
    
        if (content != post.content or title != post.title) and content and title:
            post.content = content
            post.title = title
            
            post.is_edited = True
            post.edited_at = datetime.now()
            db.session.commit()
            
            flash("Post has been successfully edited!", 'success')
        else:
            flash("Wrong content or title!", 'error')
    else:
        flash("This post cannot be edited!", 'error')
    return redirect(url_for('admin.panel', selected_action='list_posts'))

@admin_bp.route('/delete/comment/<int:id>')
@login_required
def delete_comment_form(id):
    admin = db.session.get(AdminPermission, current_user.id)
    comment = db.session.get(Comment, id)
    if not admin.remove_comments:
        flash("You have no rights to do it.", 'error')
    elif comment:
        comment.mark_as_deleted()
        db.session.commit()
        
        flash("Comment successfully deleted!", 'success')
    else:
        flash("Comment has not found.", 'error')
    
    edit = request.args.get('edit')
    return redirect(url_for('admin.panel', selected_action='list_posts', edit=edit))

@admin_bp.route('/return/comment/<int:id>')
@login_required
def return_comment_form(id):
    admin = db.session.get(AdminPermission, current_user.id)
    
    comment = db.session.get(Comment, id)
    if not admin.remove_comments:
        flash("You have no rights to do it.", 'error')
    elif comment:
        comment.mark_as_returned()
        db.session.commit()
        
        flash("Comment successfully returned!", 'success')
    else:
        flash("Comment has not found.", 'error')
        
    edit = request.args.get('edit')
    return redirect(url_for('admin.panel', selected_action='list_posts', edit=edit))

@admin_bp.route('/edit/comment/<int:id>', methods=['GET'])
@login_required
def edit_comment_form(id):
    admin = db.session.get(AdminPermission, current_user.id)
    
    comment = db.session.get(Comment, id)
    if not admin.edit_comments:
        flash("You have no rights to do it.", 'error')
    elif comment:
        params = {
            "form": CreatePostForm(),
            "content": comment.content
        }
        
        return render_template('create_post.html', id=id, header="Edit Comment as Admin", type="edit", action=url_for('admin.edit_comment', id=id), **params)
    else:
        flash("This comment cannot be edited!", 'error')
    return redirect(url_for('admin.panel', selected_action='list_posts', edit=comment.post_id))

@admin_bp.route('/edit/comment/<int:id>', methods=['POST'])
@login_required
def edit_comment(id):
    admin = db.session.get(AdminPermission, current_user.id)
    
    comment = db.session.get(Comment, id)
    if not admin.edit_comments:
        flash("You have no rights to do it.", 'error')
    elif comment:
        form = CreatePostForm()
        
        content = form.content.data
    
        if content != comment.content and content:
            comment.content = content
            
            comment.is_edited = True
            comment.edited_at = datetime.now()
            db.session.commit()
            
            flash("Comment has been successfully edited!", 'success')
        else:
            flash("Wrong content!", 'error')
    else:
        flash("This comment cannot be edited!", 'error')
    return redirect(url_for('admin.panel', selected_action='list_posts'))

@admin_bp.route('/ban_user/<int:id>')
@login_required
def ban_user(id):
    admin = db.session.get(AdminPermission, current_user.id)
    
    user = db.session.get(User, id)
    if not admin.ban_users:
        flash("You have no rights to do it.", 'error')
    elif user:
        user.mark_as_banned()
        db.session.commit()
        
        flash("User successfully banned!", 'success')
    else:
        flash("User has not found.", 'error')
    
    edit = request.args.get('edit')
    return redirect(url_for('admin.panel', selected_action='list_users', edit=edit))

@admin_bp.route('/unban_user/<int:id>')
@login_required
def unban_user(id):
    admin = db.session.get(AdminPermission, current_user.id)
    
    user = db.session.get(User, id)
    if not admin.ban_users:
        flash("You have no rights to do it.", 'error')
    elif user:
        user.mark_as_unbanned()
        db.session.commit()
        
        flash("User successfully unbanned!", 'success')
    else:
        flash("User has not found.", 'error')
        
    edit = request.args.get('edit')
    return redirect(url_for('admin.panel', selected_action='list_users', edit=edit))

@admin_bp.route('/delete/message/<int:id>')
@login_required
def delete_message_form(id):
    message = db.session.get(Message, id)
    
    edit = request.args.get('edit')
    show_full_message = request.args.get('show_full_message')
    
    if message: 
        message.mark_as_deleted()
        db.session.commit()
        
        flash("Message has been successfully deleted!", 'success')
    else:
        flash("Message has not found.", 'error')
    return redirect(url_for('admin.panel', selected_action='list_messages', edit=edit, show_full_message=show_full_message))

@admin_bp.route('/return/message/<int:id>')
@login_required
def return_message_form(id):
    message = db.session.get(Message, id)
        
    edit = request.args.get('edit')
    show_full_message = request.args.get('show_full_message')
    
    if message:
        message.mark_as_returned()
        db.session.commit()
        
        flash("Message has been successfully returned!", 'success')
    else:
        flash("Message has not found.", 'error')
    
    return redirect(url_for('admin.panel', selected_action='list_messages', edit=edit, show_full_message=show_full_message))

@admin_bp.route('edit/<int:id>', methods=['GET'])
@login_required
def edit_message(id):
    form = MessengerForm()
    
    message = db.session.get(Message, id)
    if message:
        return render_template('edit_message.html', form=form, id=id, content=message.content, other_action=url_for('admin.edit_message_submit', id=id))

@admin_bp.route('edit/<int:id>', methods=['POST'])
@login_required
def edit_message_submit(id):
    form = MessengerForm()
    
    edit = request.args.get('edit')
    show_full_message = request.args.get('show_full_message')
    
    message = db.session.get(Message, id)
    if message:
        message.content = form.content.data
        message.tag_as_edited()
        db.session.commit()
    
        flash("Successfully edited", 'success')
    else:
        flash("Can't edit this message", 'error')
    return redirect(url_for('admin.panel', selected_action='list_messages', edit=edit, show_full_message=show_full_message))


@admin_bp.route('/admins/promote/<int:id>')
@login_required
def admin_promote(id):
    user = db.session.get(User, id)
    edit = request.args.get('edit')
    
    if not user:
        flash("Can\'t find this user", 'error')
    elif user.admin_permissions:
        flash("User is already have admin rights", 'error')
    else:
        user.promote_admin()
        flash("User successfully promoted to admin with default rights", 'success')
    return redirect(url_for('admin.panel', selected_action='list_users', edit=edit))


@admin_bp.route('/admins/demote/<int:id>')
@login_required
def admin_demote(id):
    user = db.session.get(User, id)
    edit = request.args.get('edit')
    
    if not user:
        flash("Can\'t find this user", 'error')
    elif not user.admin_permissions:
        flash("User doesn\'t have admin rights", 'error')
    else:
        user.demote_admin()
        flash("User successfully demoted from admin", 'success')
    return redirect(url_for('admin.panel', selected_action='list_users', edit=edit))