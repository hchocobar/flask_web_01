from wtforms import Form
from wtforms import StringField, TextField, PasswordField,TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import HiddenField

from models import User

def length_honeypot(form,field):
	if len(field.data) > 0:
		raise validators.ValidationError("El campo debe estar vacio")

class CommentForm(Form):
	comment = TextField('Comentario',
		[
			validators.required(message="Requiere usuario"),
		])
	honeypot = HiddenField("",[length_honeypot])

class FormLogin(Form):
	username = StringField('username',
		[
			validators.length(min=4,max=35,message="Ingrese usuario valido"),
			validators.required(message="Requiere usuario")
		])
	password = PasswordField('password',
		[
			validators.length(min=4,max=35,message="Ingrese passwrod valido"),
			validators.required(message="Requiere password")
		])
	honeypot = HiddenField("",[length_honeypot])

class FormCreate(Form):
	username = StringField('username',
		[
			validators.length(min=4,max=35,message="Ingrese usuario valido"),
			validators.required(message="Requiere usuario")
		])
	email = EmailField('Correro electronico',
		[
			validators.Email()
		])
	password = PasswordField('password',
		[
			validators.length(min=4,max=35,message="Ingrese passwrod valido"),
			validators.required(message="Requiere password")
		])
	honeypot = HiddenField("",[length_honeypot])

	def validate_username(form,field):
		username =field.data
		user = User.query.filter_by(username=username).first()
		if user is not None:
			raise validators.ValidationError("El usuario ya esta en uso")

class FormNewPost(Form):
	title = StringField('Titulo',[
				validators.required('Se requiere este campo')
			])
	content = TextAreaField('Content',[
				validators.required('Se requiere este campo')
			])
	honeypot = HiddenField("",[length_honeypot])