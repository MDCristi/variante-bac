from app import app, lm, oid, db
from flask import render_template
from flask import url_for
from flask import flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from models import User, ELEV, PROFESOR
from forms import MasterForm, QuizForm, ChooseForm, QuestionForm
from app.models import *
from config import MAX_QUESTIONS
from helpers import *
# debug imports
from pprint import pprint


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
	form = QuizForm(request.form)

	# functionalitatea de submit o implementezi tot aici
	# the varinata_id member will be set right before I will add the varinta 
	# into the database
	if request.method == 'POST' and form.validate_on_submit():
		question = Question(text = str(form.question.data),
			varianta_id = None,
			question_nr = qid) 

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

# ok, it works
# after the user has chosen the desired category variants related to that 
# category will be displayed
@app.route('/choose', methods = ['GET', 'POST'])
@app.route('/choose/<category>', methods = ['GET', 'POST'])
@login_required
def choose(category = 'matematica'):
	form = ChooseForm(request.form)

	if request.method == 'POST' and form.validate_on_submit():
		return redirect(url_for('choose', 
			category = form.category.data))

	variants = Varianta.query.filter_by(category = category).all()
	pprint(variants)	
	return render_template("choose.html",
		variants = variants,
		form  = form)

@app.route('/work', methods = ['GET', 'POST'])
@app.route('/work/<int:vid>', methods = ['GET', 'POST'])
@app.route('/work/<int:vid>/<int:qid>', methods = ['GET', 'POST'])
def work(vid = 1, qid = 1):
	form = QuestionForm(request.form)

	# select the desired question
	question = Question.query.filter_by(varianta_id = vid,
		question_nr = qid).first()

	# select all the answers related to that question
	answers = Answer.query.filter_by(question_id = question.id).all()
	corerct_answers = Answer.query.filter_by(correct = 1,
		question_id = question.id).all()
	corerct_a = [corerct_answers[i].text for i in range(0, len(corerct_answers))]

	answers_values = []
	if len(answers) != 0:
		answers_values = [answers[i].text for i in range(0, 4)]

	# implement form solving here
	if 'score' not in session.keys() and qid == 1:
		session['score'] = 0

	if request.method == 'POST' and form.validate_on_submit():
		counter = 0
		items = form.data.items()
		checked_boxes = get_number_of_checked_items(form)
		print checked_boxes, "\n"
		print corerct_a, "\n"
		print answers_values, "\n"

		# he checked to many boxes
		if checked_boxes > len(answers_values):	
			# no points, reload the same page but display the flashed message
			flash('raspuns gresit')
			print "redirect to the same page \n"
			return redirect(url_for('work', vid = vid, qid = qid))

		# ia-o secvential, esti prea obosit s ate mai gandesti la algoritmi 
		# sofisticati
		if answers_values[0] in corerct_a and items[0][1] == True:
			counter += 1
		if answers_values[1] in corerct_a and items[1][1] == True:
			counter += 1
		if answers_values[2] in corerct_a and items[2][1] == True:
			counter += 1		
		if answers_values[3] in corerct_a and items[3][1] == True:
			counter += 1

		print "the value of the counter is", counter, "\n"
		if counter == len(corerct_answers):
			session['score'] += 1
			print session['score'], "\n"
			# go to the next question
			if not qid + 1 > MAX_QUESTIONS:
				return redirect(url_for('work', vid = vid, qid = qid +1 ))
			else:
				score = session['score']
				session['score'] = 0 # reset the session
				return render_template("finish.html", 
					score = score)

	return render_template("work.html", 
		question = question,
		answers = answers,
		answers_values = answers_values,
		form = form) # debug


	# % todo %
	# initilize users score
	# query teh database foor the desired quiz
	# implement quiz validation functionality
	# don't forget o build the form used for solving quizes

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