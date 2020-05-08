# ref: https://liginc.co.jp/415333

from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, logout_user, login_required, login_user
from user import User

app = Flask(__name__)

# セッション用のシークレットキー
app.secret_key = 'secret_key_hawsfiohqawefilhjwaei;fgjwilejklwerl'

# flask-loginを設定
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/', methods=['GET'])
def form():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user = User()
    login_user(user)
    return redirect(url_for('top'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# @login_requiredで要ログイン化
@app.route('/top', methods=['GET'])
@login_required
def top():
    return render_template('top.html')


@app.route('/post_from_form', methods=['POST'])
@login_required
def post_from_form():
    val = request.form["value"]
    val2 = request.form["value2"]
    print("posted value= %s, value2= %s" % (val, val2))
    return redirect(url_for('top'))

@login_manager.user_loader
def load_user(user_id):
    return User()