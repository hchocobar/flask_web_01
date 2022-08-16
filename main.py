from flask import Flask
from flask import request  # obtiene parámetros de la url. ej: /?post=1
from flask import render_template  # renderiza archivos html ubicados en /templates
from flask import make_response  # para implementación de cookies
from flask import session  # para implementar sesiones
from flask import flash  # para enviar mensajes al lado cliente
from flask import g  # para acceder a variables válidas en una misma petición, esa variable será global
from flask import redirect
from flask import url_for
from flask import copy_current_request_context
from flask_wtf import CSRFProtect  # instalar Flask_WTF para implementar CSRFProtect
from flask_mail import Mail, Message
import json  # para convertir un dict en un json
import threading  # para ejecutar en segundo plano (en este caso el envío del mail)
# Custom import
from config import DevelopmentConfig  # importamos nuestra configuración
from models import db, User, Comment  # importamos nuestras bases
from helper import date_format  # para mostrar fecha en nuestro formato
import forms  # importamos nuestros formularios


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
# implementamos secret key para evitar ataques tipo CSRF
csrf = CSRFProtect()
mail = Mail()


def send_email(user_email, username):
    msg = Message('Gracias por registrarse',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[user_email])
    msg.html = render_template('email.html',
                               username=username)
    mail.send(msg)


def create_session(username='', user_id=''):
    session['username'] = username
    session['user_id'] = user_id


# Manejo de errores - errores comunes: 503, 401, 402, 403, 404, 405, 406, 407, etc.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404  # renderizamos y como segundo parámetro enviamos el nro de error


@app.before_request
def before_request():
    # ejecuta acciones antes de ejecutar la función asociada a la url
    g.test = 'test1'  # generamos una variable global que vivirá durante la vida de nuestra petición
    if 'username' not in session and request.endpoint in ['comment']:
        error_message = 'Para realizar un comentario debes iniciar sesión'
        flash(error_message)
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['login', 'signup']:
        return redirect(url_for('index'))  # a index, porque ya tiene sesión iniciada


@app.after_request
def after_request(response):
    # ejecuta acciones posteriores a ejecutar la función asociada a la url
    return response


@app.route('/')
def index():
    title = 'Sitio Modelo'
    # custom_cookie = request.cookies.get('custom_cookie', 'Undefined')  # leemos nuestras cookies
    if 'username' in session:
        username = session['username']
    return render_template('index.html', title=title)


@app.route('/services')
def services():
    title = 'Servicios'
    list_services = ['Python Developer', 'Data Engineer', 'Serverless Apps']
    return render_template('services.html', title=title, list=list_services)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    title = 'Contáctenos'
    contact_form = forms.ContactForm(request.form)
    if request.method == 'POST' and contact_form.validate():
        pass
    return render_template('contact.html', title=title, form=contact_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Ingreso'
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data
        # verificar en la db
        user = User.query.filter_by(username=username).first()  # select * from users where username=username limit 1
        if user is not None and user.verify_password(password):
            success_message = 'Bienvenido {}'.format(username)
            flash(success_message)
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error_message = 'Usuario o contraseña inválida'
            flash(error_message)
    return render_template('login.html', title=title, form=login_form)


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')  # eliminamos la cookie 'username' de session
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = forms.SignupForm(request.form)
    if request.method == 'POST' and signup_form.validate():
        # creamos una instancia de model con los datos del formulario
        # eg 1 - envío argumentos por palabra clave
        # user = User(username=signup_form.username.data,
        #             password=signup_form.password.data,
        #             email=signup_form.email.data)
        # ex 2 - envío argumentos posicionales
        user = User(signup_form.username.data,
                    signup_form.password.data,
                    signup_form.email.data)

        # grabamos en la base de datos
        db.session.add(user)  # agregamos los datos en la instancia de SQLAlchemy
        db.session.commit()  # grabamos en la base de datos utilizando SQLAlchemy

        # enviamos un mail al usuario que se registró
        @copy_current_request_context
        def send_message(email, username):
            send_email(email, username)

        sender = threading.Thread(name='mail_sender',
                                  target=send_message,
                                  args=(user.email, user.username))
        sender.start()

        # enviamos un mensaje al front para mostrarlo en el browser
        success_message = 'Usuario registrado en la base de datos'
        flash(success_message)
    else:
        return redirect(url_for('login'))
    return render_template('signup.html', form=signup_form)


@app.route('/comment', methods=['GET', 'POST'])
def comment():
    title = 'Comentario Privado'
    comment_form = forms.CommentForm(request.form)
    if request.method == 'POST' and comment_form.validate():
        user_id = session['user_id']
        register = Comment(user_id=user_id,
                           text=comment_form.comment.data)

        db.session.add(register)
        db.session.commit()

        success_message = 'Su comentario ha sido creado'
        flash(success_message)
    else:
        pass
    return render_template('comment.html', title=title, form=comment_form)


@app.route('/reviews', methods=['GET'])
@app.route('/reviews/<int:page>', methods=['GET'])
def reviews(page=1):
    # .paginate(page=None, per_page=None, error_out=True, max_per_page=None)
    per_page = 10
    comments = Comment.query.join(User).add_columns(User.username,
                                                    Comment.text,
                                                    Comment.create_date).paginate(page, per_page, False)
    return render_template('reviews.html',
                           comments=comments,  # enviamos una variable con el contenido del comentario
                           date_format=date_format)  # enviamos una función para reformatear la fecha


@app.route('/cookie')
def cookie():
    resp = make_response(render_template('cookie.html'))  # creamos nuestro propio 'response'
    resp.set_cookie('custom_cookie', 'Prueba de Cookie')  # agregamos cookies a nuestro 'response'
    return resp


@app.route('/ajax-login', methods=['POST'])
def ajax_login():
    username = request.form['username']
    response = {'status': 200, 'username': username, 'id': 1}  # hard-code, because I haven´t DB yet!
    return json.dumps(response)


@app.route('/post')
def post():
    post_get = request.args.get('post', 'No enviaste el post')
    return 'El post es {]'.format(post_get)


if __name__ == '__main__':
    csrf.init_app(app)  # toma las configuraciones de config.py
    db.init_app(app)  # toma las configuraciones de config.py
    mail.init_app(app)  # toma las configuraciones de config.py
    with app.app_context():
        db.create_all()  # si la tabla no existe las crea, si ya existe no pasa nada
    app.run()
