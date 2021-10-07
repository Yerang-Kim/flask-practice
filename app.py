import os
from flask import Flask, render_template, request, redirect
from models import db

from models import User

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userid = request.form.get('userid')
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re-password')

        if (userid and username and password and re_password) and password == re_password:
            user = User()
            user.userId = userid
            user.userName = username
            user.password = password

            db.session.add(user)
            db.session.commit()

            return redirect('/')

    return render_template('register.html')

@app.route('/')
def hello():
    return render_template('hello.html')

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMINT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    db.app = app
    db.create_all()

    app.run(host='127.0.0.1', port=5000, debug=True)