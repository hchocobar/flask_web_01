from flask import Flask
from flask import request  # obtiene parámetros de la url. ej: /?post=1
from flask import render_template  # renderiza archivos html ubicados en /templates
from flask import make_response  # para implementación de cookies
from flask import session  # para implementar sesiones
from flask import flash  # para enviar mensajes al lado cliente

from flask import redirect
from flask import url_for

from flask_wtf import CSRFProtect  # instalar Flask_WTF para implementar CSRFProtect

import forms  # importamos nuestros formularios
import json  # para convertir un dict en un json


app = Flask(__name__)
# implementamos secret key para evitar ataques tipo CSRF
app.secret_key = 'mi_clave_secreta'  # Solo a modo de ejemplo. El secrets_key debe ser secreto
# todo mejorar el método de generación de secret_key
csrf = CSRFProtect(app)


# Manejo de errores - errores comunes: 503, 401, 402, 403, 404, 405, 406, 407, etc.
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404  # renderizamos y como segundo parámetro enviamos el nro de error


@app.route('/')
def index():
    title = 'Sitio Modelo'
    # custom_cookie = request.cookies.get('custom_cookie', 'Undefined')  # leemos nuestras cookies
    if 'username' in session:
        username = session['username']
        # todo si tenemos al cliente logueado, hacer algo
    return render_template('index.html', title=title)


@app.route('/services')
def services():
    title = 'Servicios'
    list_services = ['Python Developer', 'Data Engineer', 'Serverless Apps']
    return render_template('services.html', title=title, list=list_services)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    title = 'Contacto'
    comment_form = forms.CommentForm(request.form)
    if request.method == 'POST' and comment_form.validate():
        # todo hacer algo con los datos
        pass
    else:
        # todo error en el formulario - hacer algo
        pass
    return render_template('contact.html', title=title, form=comment_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'Ingreso'
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        success_message = 'Bienvenido {}'.format(username)
        flash(success_message)
        session['username'] = login_form.username.data

    return render_template('login.html', title=title, form=login_form)


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')  # eliminamos la cookie 'username' de session
    return redirect(url_for('login'))


@app.route('/cookie')
def cookie():
    resp = make_response(render_template('cookie.html'))  # creamos nuestro propio 'response'
    resp.set_cookie('custom_cookie', 'Prueba de Cookie')  # agregamos cookies a nuestro 'response'
    return resp


@app.route('/ajax-login', methods=['POST'])
def ajax_login():
    username = request.form['username']
    # todo aquí debo validar contra la DB
    response = {'status': 200, 'username': username, 'id': 1}  # hard-code, because I haven´t DB yet!
    return json.dumps(response)


@app.route('/post')
def post():
    post_get = request.args.get('post', 'No enviaste el post')
    return 'El post es {]'.format(post_get)


if __name__ == '__main__':
    app.run(debug=True)
