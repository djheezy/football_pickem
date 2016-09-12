
from flask_wtf import Form
from wtforms import StringField, BooleanField, RadioField
from wtforms.validators import DataRequired


class LoginForm(Form):
    user = RadioField('Name', choices=[('Brian','Brian'),
                                       ('Curt','Curt'),
                                       ('Hoke','Hoke'),
                                       ('Mike','Mike'),
                                       ('Tom','Tom')
                                       ])
    remember_me = BooleanField('Remember Me?', default=False)
