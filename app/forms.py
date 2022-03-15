from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, PasswordField, SubmitField
from wtforms.validators import InputRequired, DataRequired


class ExampleForm(FlaskForm):
	title = StringField(u'Título', validators = [InputRequired()])
	content = TextAreaField(u'Conteúdo')
	date = DateTimeField(u'Data', format='%d/%m/%Y %H:%M')
	#recaptcha = RecaptchaField(u'Recaptcha')


class LoginForm(FlaskForm):
	user = StringField(u'Usuário', validators = [InputRequired()])
	password = PasswordField(u'Senha', validators = [InputRequired()])


class AdicionarHotel(FlaskForm):
	name = StringField('Nome', validators=[DataRequired()])
	phone = StringField('Telefone', validators=[DataRequired()])
	email = StringField('E-mail', validators=[DataRequired()])
	endereco = StringField('Endereço', validators=[DataRequired()])
	numero = StringField('Número', validators=[DataRequired()])
	complemento = StringField('Complemento', validators=[DataRequired()])
	bairro = StringField('Bairro', validators=[DataRequired()])
	cidade = StringField('Cidade', validators=[DataRequired()])
	estado = StringField('Estado', validators=[DataRequired()])
	cep = StringField('CEP', validators=[DataRequired()])

	submeter = SubmitField('Submeter')
