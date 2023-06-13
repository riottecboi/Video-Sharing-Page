from flask import Flask, render_template, redirect, url_for, request, session
from flask_env import MetaFlaskEnv
from datamodel import Datamodel
from flask_wtf import CSRFProtect
import json
from redis import Redis

class Configuration(metaclass=MetaFlaskEnv):
    SECRET_KEY = "supersecretkey"
    MYSQL_HOST = "xxx"
    MYSQL_USER = "xxx"
    MYSQL_PASSWORD = "xxx"
    MYSQL_DB = "xxx"

app = Flask(__name__)
csrf = CSRFProtect(app)
redis = Redis()
try:
    app.config.from_pyfile('settings.cfg')

except FileNotFoundError:
    # Load environment variables - docker/kubernetes integration
    app.config.from_object(Configuration)

sqlconfig = {
    'host': app.config['MYSQL_HOST'],
    'user': app.config['MYSQL_USER'],
    'password': app.config['MYSQL_PASSWORD'],
    'database': app.config['MYSQL_DB']
}

db = Datamodel(sqlconfig)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home', methods=['POST','GET'])
def home():
    userLoggedin = False
    shares = db.get_video_shared()
    if 'email' in session:
        userLoggedin = True
        return render_template('main.html', userLoggedin=userLoggedin, email=session.get('email'), shares=shares)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email, loggedin = db.users(username, password)
        if not loggedin:
            return redirect(url_for('home'))
        session['email'] = email
        userLoggedin = True
        return render_template('main.html', userLoggedin=userLoggedin, email=session.get('email'), shares=shares)
    return render_template('main.html',userLoggedin=userLoggedin, shares=shares)

@app.route('/share', methods=['POST','GET'])
def share():
    if 'email' not in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        url = request.form.get('url')
        title = request.form.get('title')
        description = request.form.get('description')
        share = db.url_share(url, title, description, session.get('email'))
        message = 'New shared video from {}'.format(session.get('email'))
        redis.rpush('notifications', message)
        return redirect(url_for('home'))

    return render_template('share.html',userLoggedin=True, email=session.get('email'))

@app.route('/stream')
def stream():
    notification = redis.blpop('notifications', timeout=3)

    if notification:
        return json.dumps({'notification': notification[1].decode('utf-8')})

    return '', 204

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run()
