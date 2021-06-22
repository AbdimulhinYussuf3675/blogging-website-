from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from .forms import PitchForm,CommentForm,UpdateProfile
from ..models import User,Pitch,Comment
from .. import db,photos
import markdown2
from flask_login import login_required, current_user
import datetime
from ..requests import random_post

@main.route('/')
def index():
    '''
    View root page function that returns the index page and its data
    '''
    pitches =Pitch.query.order_by(Pitch.date.desc()).all()
    title = "Home"
    sambu = random_post()
    quote = sambu["quote"]
    quote_author = sambu ["author"]
    return render_template('index.html', title = title, pitches = pitches, quote = quote , quote_author=quote_author)

@main.route('/pitches/<category>')
def pitches_category(category):
    '''
    View function that returns blogs by category
    '''
    title = f'{category.upper()}'
    if category == "all":
        pitches = Pitch.query.order_by(Pitch.time.desc())
    else:
        pitches = Pitch.query.filter_by(category=category).order_by(Pitch.time.desc()).all()
    return render_template('pitches.html',title = title,pitches = pitches)

@main.route('/<uname>/new/pitch', methods=['GET','POST'])
@login_required
def new_pitch(uname):
    form = PitchForm()
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    title_page = "Add New Post"
    if form.validate_on_submit():
        title=form.title.data
        content=form.content.data
        category=form.category.data
        date = datetime.datetime.now()
        time = str(date.time())
        time = time[0:5]
        date = str(date)
        date = date[0:10]
        pitch = Pitch(title=title,
                      content=content,
                      category=category,
                      user=current_user,
                      date = date,
                      time = time)
        db.session.add(pitch)
        db.session.commit()
        return redirect(url_for('main.pitches_category',category = category))
    return render_template('new_pitch.html', title=title_page, form=form)

@main.route("/<uname>/pitch/<pitch_id>/new/comment", methods = ["GET","POST"])
@login_required
def new_comment(uname,pitch_id):
    user = User.query.filter_by(username = uname).first()
    pitch = Pitch.query.filter_by(id = pitch_id).first()
    form = CommentForm()
    title_page = "Comment Blog"
    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data
        date = datetime.datetime.now()
        time = str(date.time())
        time = time[0:5]
        date = str(date)
        date = date[0:10]
        new_comment = Comment(post_comment = comment, user = user, pitch = pitch,time = time, date = date )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("main.display_comments", pitch_id=pitch.id))
    return render_template("comment.html", title = title_page,form = form,pitch = pitch)

@main.route("/<pitch_id>/comments")
@login_required
def display_comments(pitch_id):
    
    pitch = Pitch.query.filter_by(id = pitch_id).first()
    title = "My Blog -- Comments"
    comments = Comment.get_comments(pitch_id)
    return render_template("display_comments.html", comments = comments,pitch = pitch,title = title)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
