from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import user_management as dbHandler
#import html  
from flask  import session
from datetime import timedelta

# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)
app.secret_key = "JIN KAZAMA"
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        if "user" in session:
         dbHandler.listFeedback()
         return render_template("/success.html", state=True, value="Back")
        else:
            return render_template("/index.html")


@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        dbHandler.insertUser(username, password, DoB)
        return render_template("/index.html")
    else:
        return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            session["user"] = username #race condition- starts a session
            session.permanent = True
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")

@app.route('/add.html', methods=['POST', 'GET'])
def add():
    if request.method=='POST':
        email = request.form['email']
        name = request.form['name']
        dbHandler.insertContact(email,name)
        return render_template('/add.html', is_done=True)
    else:
        return render_template('/add.html')


if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5000)
