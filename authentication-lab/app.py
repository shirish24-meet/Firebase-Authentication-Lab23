from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyA5XPVDNJAQwwvK2WRL3yIUXRp6hjTt78Q",
  "authDomain": "meettest-561a1.firebaseapp.com",
  "projectId": "meettest-561a1",
  "storageBucket": "meettest-561a1.appspot.com",
  "messagingSenderId": "829859778240",
  "appId": "1:829859778240:web:fdc3e3db50a90b496fe725",
  "databaseURL": "https://project-1-737be-default-rtdb.europe-west1.firebasedatabase.app/"}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
	return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		full_name = request.form['full_name']
		username = request.form['username']
		bio = request.form['bio']
		try:
			user = {"email" : email, "password" : password,"full_name" :full_name, "username" : username, "bio": bio}
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
	return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == 'POST':
		tweets = {"title":request.form['title'], "tweet" : request.form['tweet']}
		db.child("tweets").push(tweets)
	return render_template("add_tweet.html")

@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
	tweets = db.child("tweets").get().val()
	return render_template("all_tweets.html", tweets=tweets)

if __name__ == '__main__':
    app.run(debug=True)
