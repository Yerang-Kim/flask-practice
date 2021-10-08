import os
from flask import Flask, render_template, request, redirect
from wtforms.csrf.core import CSRF
from models import db
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm

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

@app.route('/')
def hello():
    return render_template('hello.html')

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