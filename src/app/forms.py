from flask.ext.wtf import Form
from wtforms import BooleanField, TextField, SelectField, IntegerField
from wtforms.validators import Required

class LoginForm(Form):
	openid = TextField('openid', validators = [Required()])
	remember_me = BooleanField('remember_me', default = False)

class MasterForm(Form):
	description = TextField('descriere', validators = [Required()])
	category = SelectField('categorie', choices = [('matematica', 'Matematica'),
		('chimie', 'Chimie')])
	
class QuizForm(Form):
	question = TextField('intrebare', validators = [Required()])
	answer_1 = TextField('raspuns1', validators = [Required()])
	answer_1_c = SelectField('raspuns_1', choices=[('true', 'adevarat'), 
		('false', 'fals')],
		 validators = [Required()])
	answer_2 = TextField('raspuns2', validators = [Required()])
	answer_2_c = SelectField('raspuns_2', choices=[('true', 'adevarat'), 
		('false', 'fals')],
		validators = [Required()])
	answer_3 = TextField('raspuns3', validators = [Required()])
	answer_3_c = SelectField('raspuns_3', choices=[('true', 'adevarat'), 
		('false', 'fals')],
		 validators = [Required()])
	answer_4 = TextField('raspuns4', validators = [Required()])
	answer_4_c = SelectField('raspuns_4', choices=[('true', 'adevarat'), 
		('false', 'fals')],
		validators = [Required()])

class ChooseForm(Form):
	category = SelectField('category', 
		# the list is not complete
		validators = [Required()],
		choices = [
			('matematica', 'Matematica'),
			('chimie', 'Chimie')
		])

# quiz solving form(s)
class QuestionForm(Form):
	option_1 = BooleanField('test', default = False)
	option_2 = BooleanField('test_2', default = False)
	option_3 = BooleanField('test_3', default = False)
	option_4 = BooleanField('test_4', default = False)
