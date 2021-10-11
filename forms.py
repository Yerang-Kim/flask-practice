from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from models import User

class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('userid', validators=[DataRequired(), EqualTo('repassword')])
    repassword  = PasswordField('repassword', validators=[DataRequired()])

class LoginForm(FlaskForm):

    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message
        
        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data
            
            user = User()
            user = user.query.filter_by(userId=userid).first()
            if user.password != password:
                raise ValueError('Wrong password')

    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('userid', validators=[DataRequired(), UserPassword()])