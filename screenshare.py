from flask import Flask, request, flash, session
from flask_bootstrap import Bootstrap
from flask.templating import render_template
import json, argparse
from screen import screenlive
from werkzeug.utils import redirect

secret_key = u'f71b10b68b1bc00019cfc50d6ee817e75d5441bd5db0bd83453b398225cede69'

app = Flask(__name__)
app.secret_key = secret_key
Bootstrap(app)

###### Landing Page ##########################################
@app.route('/')
def home():
    return render_template("home.html")

###### Viewer ##########################################
@app.route('/view')
def view():
    session.clear()
    if len(screenlive.password) == 0:
        session['access'] = True
        return render_template("screen.html")
    else:
        return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    session.clear()
    if len(screenlive.password) == 0:
        session['access'] = True
        return render_template("screen.html")

    p = request.form["password"]
    if p == screenlive.password:
        session['access'] = True
        return render_template("screen.html")
    else:
        session.clear()
        flash("Wrong password")
        return render_template("login.html")

@app.route('/screenfeed/', methods=["POST"])
def screenfeed():
    if 'access' in session and session['access']:
        return json.dumps([True, screenlive.gen()])
    else:
        return redirect('/')

###### Sharer Upload ##########################################
@app.route('/upload', methods=["POST"])
def upload():
    data = request.get_json()
    if data and 'frame' in data:
        screenlive.update(data['frame'])
        return json.dumps({"status": "ok"})
    return json.dumps({"status": "error"}), 400

### main ###
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="port, default 6100", type=int, default=6100)
    parser.add_argument("-w", "--password", help="password for viewers, default no password", default="")

    args = parser.parse_args()
    port = args.port
    screenlive.password = args.password

    app.run(host='0.0.0.0', port=port, threaded=True)
