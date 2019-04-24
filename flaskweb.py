from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '30e3b5563d6d08711e67aad45c006be6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

#Z biblioteki SQLAlchemy
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"


posts = [
	{
		'author': 'A. Beta',
		'title': 'Witam',
		'content': 'First post content',
		'date_posted': 'April 20, 2018'
	},
	{
		'author': 'C. Delta',
		'title': 'Pozdrawiam',
		'content': 'Second post content',
		'date_posted': 'April 21, 2018'
	}
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():

		#Dodanie użytkownika do bazy danych na podstawie wprowadzonych w formularzu rejestracji danych
		user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user) 
		db.session.commit()

		flash(f'Mamy Twoje dane {form.username.data} #RODO', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		
		user = User.query.filter_by(email=form.email.data).first()
		
		if user and user.password == form.password.data:
			login_user(user, remember=form.remember.data)
			return redirect(url_for('home'))
			
		else:
			flash('Logged in unsuccessfully!', 'danger')

	return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
   	app.run(debug=True)