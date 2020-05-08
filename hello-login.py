from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, logout_user
app = Flask(__name__)

# flask-loginを設定
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/', methods=['GET'])
def form():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('top.html')