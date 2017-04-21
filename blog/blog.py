
from flask import (
	Flask,
	render_template,
	request,
	redirect,
	url_for,
	# http session
	session 
)


from flask.ext.sqlalchemy import SQLAlchemy

import datetime


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'zjx2029799'
db = SQLAlchemy(app)


class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	posts = db.relationship('Post', backref='author', lazy='dynamic' )


class Post(db.Model):
	__tablename__ = 'post'
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(600))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


db.create_all()
db.session.commit()



@app.route('/')
def index():
	if 'username' in session:
		user = User.query.filter_by(username=session['username']).first()
		if not user:
			session.pop('username', None)
			return render_template('index.html.jinja')
		blogs = user.posts.all()
		return render_template('index.html.jinja', user=user, blogs=blogs)
	return render_template('index.html.jinja')

@app.route('/signup', methods=['GET','POST'])
def signup():
	if request.method == 'POST':
		username = request.form['username']
		user = User(username=username)
		db.session.add(user)
		db.session.commit()
		session['username'] = username
		return redirect(url_for('index'))
	return render_template('signup.html.jinja')

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		session['username'] = username
		return redirect(url_for('index'))

	return render_template('login.html.jinja')

@app.route('/create', methods=['GET','POST'])
def create():
	if request.method == 'POST':
		content = request.form['content']
		user = User.query.filter_by(username=session['username']).first()
		post = Post(content=content, timestamp=datetime.datetime.utcnow(), author=user)
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('create.html.jinja')

@app.route('/logout')
def logout():
	session.pop('username',None)
	return redirect(url_for('index'))
	return 200

@app.route('/:other')
def other():
	return render_template('404.html.jinja')

app.run(debug=True)