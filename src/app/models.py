from app import db

ELEV = 0
PROFESOR = 1

class User(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	name = db.Column(db.String(60), index = True, unique = True)
	email = db.Column(db.String(140), index = True, unique = True)
	role = db.Column(db.SmallInteger, default = ELEV)
	variante = db.relationship('Varianta', backref = 'author', lazy = 'dynamic')

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.name)

# Tabele relatate unei variante
class Varianta(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	valide = db.Column(db.Boolean())
	description = db.Column(db.String(80))
	category = db.Column(db.String(80))
	user_id = db.Column(db.SmallInteger(), db.ForeignKey('user.id'))
	question = db.relationship('Question', backref='author')

class Question(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	text = db.Column(db.String(500))
	question_nr = db.Column(db.Integer())
	varianta_id = db.Column(db.Integer(), db.ForeignKey('varianta.id')) 
	answer = db.relationship('Answer', backref = 'author')

class Answer(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	text = db.Column(db.String(500))
	correct = db.Column(db.Boolean())
	question_id = db.Column(db.Integer, db.ForeignKey('question.id'))