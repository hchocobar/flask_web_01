from wtforms import Form
from wtforms.fields import StringField, TextAreaField, EmailField, HiddenField, PasswordField
from wtforms import validators
from models import User

def lenght_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('El campo debe estar vacío')


class ContactForm(Form):
    name = StringField('Nombre y Apellido',
                       [validators.InputRequired(message='El campo es requerido'),
                        validators.Length(min=8, max=25, message='El nombre de usuario debe tener un mínimo de 8 '
                                                                 'caracteres y un máximo de 25')])
    email = EmailField('Correo electrónico',
                       [validators.InputRequired(message='El email es requerido'),
                        validators.Length(min=4, max=50, message='Ingrese un email válido')])
    consult = TextAreaField('Consulta')
    # este campo es para evitar el spam en el formulario
    honeypot = HiddenField('', [lenght_honeypot])


class CommentForm(Form):
    comment = TextAreaField('Comentario',
                            [validators.InputRequired(message='Comentario vacío')])
    # este campo es para evitar el spam en el formulario
    honeypot = HiddenField('', [lenght_honeypot])


class LoginForm(Form):
    username = StringField('Username',
                           [validators.InputRequired(message='El nombre de usuario es requerido'),
                            validators.Length(min=8, max=25, message='El nombre de usuario debe tener un mínimo de 8 '
                                                                     'caracteres y un máximo de 25')])
    password = PasswordField('Password',
                             [validators.InputRequired(message='El password es requerido')])
    honeypot = HiddenField('', [lenght_honeypot])


class SignupForm(Form):
    username = StringField('Username',
                           [validators.InputRequired(message='El nombre de usuario es requerido'),
                            validators.Length(min=8, max=25, message='El nombre de usuario debe tener un mínimo de 8 '
                                                                     'caracteres y un máximo de 25')])
    email = EmailField('Correo electrónico',
                       [validators.InputRequired(message='El email es requerido'),
                        validators.Length(min=4, max=50, message='Ingrese un email válido')])
    # validators.Email(message='Ingrese un email válido'),
    password = PasswordField('Password',
                             [validators.InputRequired(message='El password es requerido')])

    def validate_username(form, field):  # realizo overwrite del método validate de username
        username = field.data
        user = User.query.filter_by(username=username).first()
        if user is not None:
            raise validators.ValidationError('Ese username no está disponible')
