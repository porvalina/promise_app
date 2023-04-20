from flask import Flask, render_template, url_for, request, session, redirect, flash
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm

app = Flask(__name__)

menu = [{"name": "My promises", "url": "/promiseList"},
        {"name": "Create new promise", "url": "/createPromise"},
        {"name": "log out", "url": "/logout"}]

app.config['SECRET_KEY'] = 'QWERTY987VBNM2209'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Session(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/profile/", methods=["GET", "POST"])
def profile(): 
    if request.method == 'POST':
            if len(request.form['promise']) > 1:
                flash('Your promise is created!Good luck!', category='success')
            else:
                flash('Add steps to achieve your dream!', category='error')
    print(request.form)
    session["numberOfTasks"] = 1
    return render_template('createPromise.html', numberOfTasks = session["numberOfTasks"], menu=menu)

@app.route("/addTask", methods=["GET"])
def addTask():
    session["numberOfTasks"] = session["numberOfTasks"] + 1
    return render_template('createPromise.html', numberOfTasks = session["numberOfTasks"])

@app.route('/createPromise')
def createPromise():
    return render_template('createPromise.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@app.route('/logout')
def logout():
    session['userLogged'] = None
    # return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/promiseList')
def promiseList():
    return render_template('promiseList.html')

@app.route("/login", methods=["POST", "GET"])
def login():
     print('LOGIN')
     if 'userLogged' in session:
          print('WE HAVE USER IN SESSION')
          return redirect(url_for('profile', username=session['userLogged']))
     
     if request.method == 'POST':
        print('Try to login with ' + request.form['username'])
        user = User.query.filter_by(username=request.form['username'], password=request.form['psw']).first()
        print(user)
        print(user.username)
        if len(user) == 0:
            return render_template('login.html') 
        
        
        session['userLogged'] = user.username
        return redirect(url_for('profile' , username=session['userLogged']))
     

     print('RENDER LOGIN FORM')
     return render_template('login.html') 

     

@app.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(username=form.username.data, email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit
        flash('Thanks for registering')
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True) 
  username = db.Column(db.String(64))
  email = db.Column(db.String(64), unique=True)
  password = db.Column(db.String(64))
#   users = db.relationship('User', backref='',lazy='dynamic')

  def __repr__(self):
    return '<User %r>' % self.username

@app.errorhandler(404)
def pageNotFound(error):
     return render_template('page404.html'), 404

if __name__=="__main__":
    app.run(debug=True)