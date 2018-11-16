
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from wtforms.validators import Required

class PitchingForm(FlaskForm):

    title = StringField('Pitching title',validators=[Required()])
    category = SelectField('Category', choices=[('1','Production'),('2','Interview'),('3','Promotion')])
    submit = SubmitField('Submit')
    content = TextAreaField('Your Pitch', validators=[Required()])

class UpdateProfile(FlaskForm):
    name =  StringField('Category Name', validators=[Required()])
    submit = SubmitField('Create')

class CommentForm(FlaskForm):
    opinion = TextAreaField('WRITE A COMMENT')
    submit = SubmitField('SUBMIT')