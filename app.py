import os
from flask import Flask, render_template, request, redirect, session
from wtforms.csrf.core import CSRF
from models import db
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm

from models import User

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User()
        user.userId = form.data.get('userid')
        user.userName = form.data.get('username')
        user.password = form.data.get('password')

        db.session.add(user)
        db.session.commit()

        print('Success!')

        return redirect('/')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        session['userid'] = form.data.get('userid')

        return redirect('/')
    
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')

@app.route('/')
def hello():
    userid = session.get('userid', None)
    return render_template('hello.html', userid=userid)

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMINT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'sjsjijejiwcwqw'

    csrf = CSRFProtect()
    csrf.init_app(app)
    db.init_app(app)
    db.app = app
    db.create_all()

    app.run(host='127.0.0.1', port=5000, debug=True)