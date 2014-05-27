from app import app, lm, oid, db
from flask import render_template
from flask import url_for
from flask import flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import User, ELEV, PROFESOR
from forms import MasterForm, QuizForm
from app.models import *
from config import MAX_QUESTIONS
from helpers import boolean_value

# on dev
@app.before_request
def before_request():
    g.user = current_user

# on dev
@app.route('/')
@app.route('/index')
def index():
	# use debug var for testing
	user = g.user
	return render_template('index.html',
		user = user)

# on dev
@app.route('/varianta')
def varianta():
	return "nimic inca"

# on dev
@app.route('/cuprieten')
def cuprieten():
	return "nimic inca"

# on dev
@app.route('/creeaza', methods = ['GET', 'POST'])
@login_required
def creeaza():
	form = MasterForm()
	if form.validate_on_submit():
		# export data for the next step
		session['form_description'] = str(form.description.data)
		session['form_category'] = str(form.category.data)
		session['varianta'] = Varianta(description = session['form_description'],
			category = str(form.category.data),
			valide = False,
			user_id = g.user.id) 

		db.session.add(session['varianta'])
		db.session.commit()

		return redirect(url_for('build'))

	return render_template('creeaza.html',
		form = form)

# fiecare intrebare are forma <intrabre>_<id>
# fiecare raspuns are forma  <id intrebare>_<raspuns>_<id>
# fiecare select cu valoarea de adevar a unui raspuns are forma
#    id intrebare>_<raspuns>_<id>-c, c vine de la correctness
#
#! cu chiu, cu vai, maerge
@app.route('/build', methods = ['GET', 'POST'])
@app.route('/build/<int:qid>', methods = ['GET', 'POST'])
@login_required
def build(qid = 1):
	if session['form_description'] is None or qid > MAX_QUESTIONS:
		flash('Ai accesat o pagina invalida')
		return redirect(url_for('creeaza'))

	# build dynamically the form
	form = QuizForm()

	# functionalitatea de submit o implementezi tot aici
	# the varinata_id member will be set right before I will add the varinta 
	# into the database
	if request.method == 'POST' and form.validate_on_submit():
		question = Question(text = str(form.question.data),
			varianta_id = None) 

		answer_1 = Answer(text = str(form.answer_1.data),
			question_id = question.id,
			correct = boolean_value(form.answer_1_c.data))
		answer_2 = Answer(text = str(form.answer_1.data),
			question_id = question.id,
			correct = boolean_value(form.answer_2_c.data))
		answer_3 = Answer(text = str(form.answer_1.data),
			question_id = question.id,
			correct = boolean_value(form.answer_3_c.data))
		answer_4 = Answer(text = str(form.answer_1.data),
			question_id = question.id,
			correct = boolean_value(form.answer_4_c.data))

		# add the records into database
		# be careful, if the user does not complete the quiz you have pieces
		# of an incomplete quiz, thus you should add an extra field to the
		# varianta class, and you will set that field to True if the quiz in 
		# valide or False instead
		db.session.add(session['varianta'])
		db.session.commit()
		varianta = Varianta.query.filter_by(
			description = session['varianta'].description,
			category = session['varianta'].category,
			user_id = session['varianta'].user_id).first()

		question.varianta_id = varianta.id
		db.session.add(question)
		db.session.commit()

		question_id = Question.query.filter_by(
			text = question.text,
			varianta_id = varianta.id).first()

		answer_1.question_id = question_id.id
		answer_2.question_id = question_id.id
		answer_3.question_id = question_id.id
		answer_4.question_id = question_id.id

		db.session.add(answer_1)
		db.session.add(answer_2)
		db.session.add(answer_3)
		db.session.add(answer_4)

		db.session.commit()
		
		if qid == MAX_QUESTIONS:

			varianta.valide = True
			db.session.add(varianta)
			db.session.commit()

			flash('verifica baza de date')
			return redirect(url_for('creeaza'))
			
		return redirect(url_for('build', qid = qid + 1))
	else:
		flash(form.errors)

	print "randez build.html ",
	return render_template('build.html', 
		form = form)


# on dev
@app.route('/choose')
@login_required
def choose():
	variante = Varianta.query.get

#on dev
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
	return oid.try_login('https://www.google.com/accounts/o8/id', 
		ask_for = ['nickname', 'email'])

# on dev
@oid.after_login
def after_login(resp):
	if resp.email is None or resp.email == "":
		flash("invalid email")
		return redirect(url_for('debug'))

	user = User.query.filter_by(email = resp.email).first()
	if user is None:
		nickname = resp.nickname
		if nickname is None or nickname == "":
			nickname = resp.email.split('@')[0] 
		user = User(name = nickname, email = resp.email, role = ELEV)
		db.session.add(user)
		db.session.commit()
	
	login_user(user)
	return redirect(request.args.get('next') or url_for('debug')) # debug

@app.route('/logout')
def logout():
	logout_user()
	flash("gata nu mai esti logat")
	return redirect(url_for('index'))

# on dev
@lm.user_loader
def load_user(id):
	return User.query.get(int(id))	