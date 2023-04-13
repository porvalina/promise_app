from flask import Flask, render_template, url_for, request, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/')
def index():
   
    return render_template('index.html')

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == 'POST':
        print(request.form)
    session["numberOfTasks"] = 1
    return render_template('createPromise.html', numberOfTasks = session["numberOfTasks"])

@app.route("/addTask", methods=["GET"])
def addTask():
    session["numberOfTasks"] = session["numberOfTasks"] + 1
    return render_template('createPromise.html', numberOfTasks = session["numberOfTasks"])



if __name__=="__main__":
    app.run(debug=True)