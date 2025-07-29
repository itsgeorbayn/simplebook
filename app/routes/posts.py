from flask import Blueprint, render_template, redirect, url_for, flash, current_app, jsonify, request, session
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import CreatePostForm, AddCommentForm
from app.models import User, Post, Comment, Like, UserVerification, Report
from app.extensions import db, login_manager
from app.utils import to_sentence_case, is_email_or_username, generate_random_text, Symbols, check_verify_status, require_not_banned, fix_img_src_paths
from datetime import datetime
from werkzeug.utils import secure_filename
import os, unicodedata, re, random, uuid

posts_bp = Blueprint('posts', __name__, url_prefix='/posts')

@posts_bp.route('/create', methods=['GET'])
@login_required
@require_not_banned
def create_post_form():
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    params = {
        "form": CreatePostForm()
    }
    
    return render_template('create_post.html', show_title=True, header="Create Post", **params)

@posts_bp.route('/create', methods=['POST'])
@login_required
@require_not_banned
def create_post_submit():
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    form = CreatePostForm()
    
    title = Symbols.clean_title(form.title.data)
    slug = Symbols.slug()
    content = fix_img_src_paths(form.content.data)
    
    post = Post(author_id=current_user.id, title=title, slug=slug, content=content, created_at=datetime.now())
    if post and content:
        db.session.add(post)
        db.session.commit()
        
        flash("Post has been successfully created!", 'success')
        
        post.send_news()
    else:
        flash("Post cannot be created", 'error')
        
    return redirect(url_for('profile.profile'))
    
# @posts_bp.route('/upload-image', methods=['POST'])
# @login_required
# @require_not_banned
# def upload_image():
#     file = request.files.get('file')
#     if not file:
#         return jsonify({'error': 'No file uploaded'}), 400

#     filename = secure_filename(file.filename)
#     ext = os.path.splitext(filename)[1].lower()

#     if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
#         flash("Invalid file format", 'error')
#         return redirect(url_for('create_post'))

#     unique_name = f"{uuid.uuid4().hex}{ext}"
#     save_path = f'app/static/uploads/{unique_name}'
#     file.save(save_path)

#     file_url = url_for('static', filename=f'uploads/{unique_name}', _external=False)
    return jsonify({'location': file_url})

@posts_bp.route('/add_comment', methods=['GET'])
@login_required
@require_not_banned
def add_comment_form():
    post_id = request.args.get('post_id')
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    form = AddCommentForm()
    
    return render_template('add_comment.html', show_title=False, post_id=post_id, form=form, header="Add Comment")

@posts_bp.route('/add_comment', methods=['POST'])
@login_required
@require_not_banned
def add_comment_submit():
    post_id = int(request.args.get('post_id'))
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    form = AddCommentForm()
    
    if form.validate_on_submit():
        params = {
            "author_id": current_user.id,
            "post_id": int(request.args.get('post_id')),
            "content": request.form.get('content'),
            "created_at": datetime.now()
        }
        
        new_comment = Comment(**params)
        db.session.add(new_comment)
        db.session.commit()
        
        flash("Comment successfully created.", 'success')
    else:
        flash("Something went wrong while proceeding your comment, try again later.", 'error')
    
    author_id = db.session.get(Post, post_id).author_id
    if author_id == current_user.id:
        return redirect(url_for('profile.profile'))
    return redirect(url_for('friends.friends_profile', friend_id=author_id))

@posts_bp.route('/like/<int:id>')
@login_required
def like_post_form(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    post = db.session.get(Post, id)
    if post:
        like = db.session.query(Like).filter_by(user_id=current_user.id, post_id=id).first()
        
        if like:
            db.session.delete(like)
        else:
            new_like = Like(user_id=current_user.id, post_id=id, created_at=datetime.now())
            
            db.session.add(new_like)
        db.session.commit()
        
        if current_user.id == post.author.id:
            return redirect(url_for('profile.profile'))
        return redirect(url_for('friends.friends_profile', friend_id=post.author.id))
    
@posts_bp.route('/delete/<int:id>')
@login_required
@require_not_banned
def delete_post_form(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    post = db.session.get(Post, id)
    if post:
        if post.author_id != current_user.id:
            is_own = False
            flash("This is not your post!", 'error')
        else:
            is_own = True
            
            post.mark_as_deleted()
            db.session.commit()
            
            flash("Post has been successfully deleted!", 'success')
            
            post.delete_news()

        if not is_own:
            return redirect(url_for('friends.friends_profile', friend_id=post.author.id))
    else:
        flash("Post has not found.", 'error')
    return redirect(url_for('profile.profile'))

@posts_bp.route('/return/<int:id>')
@login_required
@require_not_banned
def return_post_form(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    post = db.session.get(Post, id)
    if post:
        if post.author_id != current_user.id:
            is_own = False
            flash("This is not your post!", 'error')
        else:
            is_own = True
            
            post.mark_as_returned()
            db.session.commit()
            
            flash("Post has been successfully returned!", 'success')
            
            post.send_news(return_news=True)
        if not is_own:
            return redirect(url_for('friends.friends_profile', friend_id=post.author.id))
    else:
        flash("Post has not found.", 'error')
    return redirect(url_for('profile.profile'))

@posts_bp.route('/repost/<int:id>')
@login_required
@require_not_banned
def repost_form(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    post = db.session.get(Post, id)
    if post:
        if post.author_id == current_user.id:
            if post.reference:
                flash("You can\'t repost your own repost!", 'error')
            else:
                flash("You can\'t repost your own post!", 'error')
        else:
            prev = db.session.query(Post).filter_by(author_id=current_user.id, reference=id, is_deleted=False).first()
            if prev:
                flash("Previous repost of this post deleted.", 'warning')
                prev.mark_as_deleted()
                
            new_post = Post(content=post.content, created_at=post.created_at, author_id=current_user.id, title=post.title, slug=Symbols.slug())
            new_post.tag_as_reposted(id=post.id)

            db.session.add(new_post)
            db.session.flush()

            if prev:
                comments = db.session.query(Comment).filter_by(post_id=prev.id).all()
                for comment in comments:
                    comment.post_id = new_post.id
                    comment.is_migrated = True
            
            db.session.commit()
            
            flash("Post has been successfully reposted.", 'success')
    else:
        flash("Post has not found.", 'error')
    return redirect(url_for('profile.profile'))

@posts_bp.route('/edit/<int:id>', methods=['GET'])
@login_required
@require_not_banned
def edit_post_form(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    post = db.session.get(Post, id)
    if post and post.author_id == current_user.id and not post.is_reposted:
        params = {
            "form": CreatePostForm(),
            "title": post.title,
            "content": post.content
        }
        
        return render_template('create_post.html', id=id, show_title=True, header="Edit Post", type="edit", action=url_for('posts.edit_post', id=id), **params)
    flash("This post cannot be edited!", 'error')
    return redirect(url_for('profile.profile'))

@posts_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
@require_not_banned
def edit_post(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    post = db.session.get(Post, id)
    if post and post.author_id == current_user.id and not post.is_reposted:
        form = CreatePostForm()
        
        title = Symbols.clean_title(form.title.data)
        content = fix_img_src_paths(form.content.data)
    
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
    return redirect(url_for('profile.profile'))

@posts_bp.route('/edit/comment/<int:id>', methods=['GET'])
@login_required
@require_not_banned
def edit_comment_form(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    comment = db.session.get(Comment, id)
    if comment and comment.author_id == current_user.id:
        params = {
            "form": CreatePostForm(),
            "content": comment.content
        }
        
        return render_template('create_post.html', id=id, header="Edit Comment", type="edit", action=url_for('posts.edit_comment', id=id), **params)
    flash("This comment cannot be edited!", 'error')
    return redirect(url_for('profile.profile'))

@posts_bp.route('/edit/comment/<int:id>', methods=['POST'])
@login_required
@require_not_banned
def edit_comment(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    comment = db.session.get(Comment, id)
    if comment and comment.author_id == current_user.id:
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
    return redirect(url_for('profile.profile'))

@posts_bp.route('/delete/comment/<id>', methods=['GET'])
@login_required
@require_not_banned
def delete_comment(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    comment = db.session.get(Comment, id)
    post_author_id = comment.post.author_id
    is_allowed_to_delete_comment = False
    
    if not comment:
        flash("Can\'t find this post", 'error')
    elif post_author_id == current_user.id:
        is_allowed_to_delete_comment = True
    elif comment.author_id != current_user.id:
        flash("You can\'t delete this message.", 'error')
    elif comment.is_deleted:
        flash("This post is already deleted.", 'error')
    else:
        is_allowed_to_delete_comment = True
    
    if is_allowed_to_delete_comment:
        flash("Comment successfully deleted.", 'success')
        
        comment.mark_as_deleted()
        db.session.commit()

    if current_user.id == post_author_id:
        return redirect(url_for('profile.profile'))
    return redirect(url_for('friends.friends_profile', friend_id=post_author_id))

@posts_bp.route('/report/post/<int:id>', methods=['GET'])
@login_required
@require_not_banned
def report_post(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    post = db.session.get(Post, id)
        
    if not post:
        flash("Can\'t find this post", 'error')
    elif post.author_id == current_user.id:
        flash("You can\'t report your own post.", 'error')
    elif post.is_deleted:
        flash("This post is deleted.", 'error')
    else:
        prev_report = db.session.query(Report).filter_by(author_id=current_user.id, reference_table="posts", reference_id=post.id).first()
        if prev_report:
            db.session.delete(prev_report)
            flash("Successfully unreported", 'success')
        else:
            report = Report(author_id=current_user.id, reference_table="posts", reference_id=post.id)
            db.session.add(report)
            flash("Successfully reported", 'success')
        db.session.commit()
    
    return redirect(session.get('history', [])[-2])

@posts_bp.route('/report/comment/<int:id>', methods=['GET'])
@login_required
@require_not_banned
def report_comment(id):
    verify_status = check_verify_status()
    if verify_status:
        return verify_status
    
    comment = db.session.get(Comment, id)
        
    if not comment:
        flash("Can\'t find this comment", 'error')
    elif comment.author_id == current_user.id:
        flash("You can\'t report your own comment.", 'error')
    elif comment.is_deleted:
        flash("This comment is deleted.", 'error')
    else:
        prev_report = db.session.query(Report).filter_by(author_id=current_user.id, reference_table="comments", reference_id=comment.id).first()
        if prev_report:
            db.session.delete(prev_report)
            flash("Successfully unreported", 'success')
        else:
            report = Report(author_id=current_user.id, reference_table="comments", reference_id=comment.id)
            db.session.add(report)
            flash("Successfully reported", 'success')
        db.session.commit()
    
    return redirect(session.get('history', [])[-2])