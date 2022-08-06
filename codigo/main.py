from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from flask import make_response
from werkzeug.utils import secure_filename

import json
import os

# protection
from flask_wtf import CSRFProtect

import forms
from helper import date_format
from helper import featurepagination, extract_text, delete_spacewith

from models import db
from models import User
from models import Comment
from models import Post

from config import DevelopmentConfig

UPLOAD_FOLDER = '/home/jc/Flask/flask_ejemplo/static/img/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
# app = Flask(__name__,template_folder ='prueba')

app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['comment', 'new_post']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['login', 'create']:
        return redirect(url_for('index'))


@app.after_request
def after_request(response):
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    loginform = forms.FormLogin(request.form)
    if request.method == 'POST' and loginform.validate():
        username = loginform.username.data
        password = loginform.password.data

        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            success_messages = "Bienvenido {}".format(username)
            flash(success_messages)
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error_message = 'usuario no valido'
            flash(error_message)

        session['username'] = loginform.username.data

    title = "Curso flask login"
    return render_template('login.html', title=title, form=loginform)


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('index'))


@app.route('/cookie')
def cookie():
    response = make_response(render_template('cookie.html'))
    response.set_cookie('custom_cookie', 'jose')
    return response


@app.route('/')
def index():
    custom_cookie = request.cookies.get('custom_cookie')
    if 'username' in session:
        username = session['username']

    posts_list = Post.query.join(User).add_columns(User.username, Post.id, Post.title, Post.content,
                                                   Post.create_date).paginate(1, 10, False)

    title = "Curso flask"
    return render_template('index.html', title=title, posts=posts_list, date_format=date_format,
                           extract_text=extract_text, delete_spacewith=delete_spacewith)


@app.route('/post/<int:id>/<title>', methods=['GET', 'POST'])
def post(id, title):
    post = Post.query.filter_by(id=id).first()
    comment_form = forms.CommentForm(request.form)

    if request.method == 'POST' and comment_form.validate():
        user_id = User.query.filter_by(username=session['username']).first()
        comment = Comment(user_id=user_id.id, text=comment_form.comment.data, posts_id=id)
        db.session.add(comment)
        db.session.commit()

    comment_list = User.query.join(Comment).join(Post).filter_by(id=id).add_columns(Comment.user_id, User.username,
                                                                                    Comment.text,
                                                                                    Comment.create_date).paginate(1,
                                                                                                                  1000,
                                                                                                                  False)
    return render_template('post.html', post=post, form=comment_form, date_format=date_format, comments=comment_list)


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    comment_form = forms.CommentForm(request.form)
    if request.method == 'POST' and comment_form.validate():
        user_id = User.query.filter_by(username=session['username']).first()
        # print user_id.id
        comment = Comment(user_id=user_id.id, text=comment_form.comment.data)
        db.session.add(comment)
        db.session.commit()

    title = "comments"
    return render_template('comment.html', title=title, form=comment_form)


@app.route('/reviews/<int:page>', methods=['GET'])
@app.route('/reviews/', methods=['GET'])
def reviews(page=1):
    per_page = 3
    comment_list = Comment.query.join(User).add_columns(User.username, Comment.text, Comment.create_date).paginate(page,
                                                                                                                   per_page,
                                                                                                                   False)
    num_comm = Comment.query.count()
    pag = featurepagination(page, num_comm, per_page)
    return render_template('reviews.html', comments=comment_list, date_format=date_format, num=num_comm, pag=pag,
                           page=page)


@app.route('/create', methods=['GET', 'POST'])
def create():
    createform = forms.FormCreate(request.form)
    if request.method == 'POST' and createform.validate():
        user = User(createform.username.data,
                    createform.email.data,
                    createform.password.data)

        db.session.add(user)
        db.session.commit()

        success_messages = 'Usuario registrado en la base de datos'
        flash(success_messages)
    return render_template('create.html', title='Create', form=createform)


@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    postform = forms.FormNewPost(request.form)
    if request.method == 'POST' and postform.validate():
        user_id = User.query.filter_by(username=session['username']).first()
        posts = Post(user_id=user_id.id, title=postform.title.data, content=postform.content.data)

        db.session.add(posts)
        db.session.commit()

        success_messages = 'Post guardado'
        flash(success_messages)

    return render_template('newpost.html', form=postform)


@app.route('/ajax-login', methods=['POST'])
def ajax_login():
    # print request.form['username']
    print(request.form['username'])
    username = request.form['username']
    response = {'status': 200, 'username': username, 'id': 1}
    return json.dumps(response)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return render_template('img.html')


if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(port=8000)
