from . import main
from flask import render_template,request,redirect,url_for,abort,flash
from flask_login import login_required,current_user
from ..models import User,Post
from .forms import UpdateProfile,PostForm
from .. import db,photos


# Views

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    
    title = 'Home - Welcome to my blog'
    return render_template('index.html', title = title)

@main.route('/post/new',methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title = form.title.data, content = content.form.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('.home'))
    title = 'New Post' 
    return render_template('posts.html',title = title,form = form)

@main.route('/home', methods = ['GET','POST'])
def home():
    '''
    View root page function that returns the home page and its data
    '''
    posts = Post.query.all()
    title = 'Home - Welcome to My BLog'
    return render_template('home.html', title = title, posts = posts)


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