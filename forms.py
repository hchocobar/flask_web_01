from wtforms import Form
from wtforms.fields import StringField, TextAreaField, EmailField, HiddenField, PasswordField
from wtforms import validators


def lenght_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('El campo debe estar vacío')


class CommentForm(Form):
    username = StringField('username',
                           [validators.DataRequired(message='El campo es requerido'),
                            validators.length(min=8, max=25, message='El nombre de usuario debe tener un mínimo de 8 '
                                                                     'caracteres y un máximo de 25')
                            ])
    email = EmailField('Correo electrónico', [validators.DataRequired(message='El campo es requerido')])
                                              # validators.Email(message='ingrese un email válido')
    comment = TextAreaField('Comentario')
    # este campo es para evitar el spam en el formulario
    honeypot = HiddenField('', [lenght_honeypot])


class LoginForm(Form):
    username = StringField('Username',
                           [validators.DataRequired(message='El nombre de usuario es requerido'),
                            validators.length(min=8, max=25, message='Ingrese el nombre un username válido')])
    password = PasswordField('Password',
                             [validators.DataRequired(message='El password es requerido')])
    honeypot = HiddenField('', [lenght_honeypot])


""" Validaciones
- Agregar validaciones en la creación de los campos en la clase (forms.py)
- Agregar el condicional .validate() en main.py
- Mostrar los field.errors en _macro.html 
"""

""" honeypot (una forma de prevenir el spam en los formularios)
- Agregar el atributo en la clase (form.py)
- Agregar el campo en el formulario (contact.html / blog.html) 
"""