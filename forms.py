from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired

class SurveyForm(FlaskForm):
    question1 = RadioField("Indoors or Outdoors",choices=[("id1","Indoors"),("id2","Outdoors and indoors"),("id3","Outdoors")], validators=[DataRequired()])
    question2 = RadioField("Hot or Cold Climate",choices=[("id1","Hot"),("id2","Warm"),("id3","Cold")], validators=[DataRequired()])
    question3 = RadioField("Physical or Sedentary",choices=[("id1","Physical"),("id2","some physical activity and sedentary"),("id3","Sedentary")], validators=[DataRequired()])
    question4 = RadioField("Far or close to home",choices=[("id1","Close (<50 miles)"),("id2","Far (>50 miles)")], validators=[DataRequired()])
    address = StringField("Home address (Town, State)", validators=[DataRequired()])
    my_submit = SubmitField("Plan Route")
