from flask import Flask, render_template, jsonify, url_for, redirect, request
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy 

from forms import SurveyForm

import requests
import json
import pathlib
import textwrap
import google.generativeai as genai


genai.configure(api_key="AIzaSyCYMJbDw6D6GWk7bg_Ux5VQOTdqReAEvUk")
model = genai.GenerativeModel('gemini-1.5-flash')



app = Flask(__name__)
app.config["SECRET_KEY"] = "hackathonnum2"

socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

prompt = "This person likes the following "

db = SQLAlchemy(app)

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    guide_text = db.Column(db.Text)

with app.app_context():
    db.create_all()

@app.route('/',methods=["GET","POST"])
def home():
    user_survey = SurveyForm()
    if user_survey.validate_on_submit():
        question1answer = dict(user_survey.question1.choices).get(user_survey.question1.data)
        question2answer = dict(user_survey.question2.choices).get(user_survey.question2.data)
        question3answer = dict(user_survey.question3.choices).get(user_survey.question3.data)
        question4answer = dict(user_survey.question4.choices).get(user_survey.question4.data)
        prompt = """A person home address is"""+user_survey.address.data+""" and likes 
        these vacation spot traits: """+question1answer+","+question2answer+" climate, involves "+question3answer+","+question4answer+""", from home (close < 2 hour away driving | far >= 2 hour away driving).
        Return the coordinates of the home address as the first index in the array, and coordinates of 3 other vacation locations that are suitable for the vacation traits. Provide only an array of coordinates in this format [{"lat":0,0,"lng":0,0}] with no commentary or additional text"""
        response = model.generate_content(prompt)
        
        modifiedtext = response.text.replace("`","")
        modifiedtext = modifiedtext.replace("json","")

        guideText = model.generate_content("""Based off the last 3 coordinates, of places, in the array:"""+modifiedtext+""". Now pretend your a person (dont break cahracter)
        that is breifly telling someone to visit these places, in no particular order, by name.""")

        print(modifiedtext)
        new_route = Route(text=modifiedtext, guide_text=guideText.text)
        db.session.add(new_route)
        db.session.commit()
        return redirect(url_for('trip_map'))
    return render_template("index.html",template_form=user_survey)

@app.route('/trip_map')
def trip_map():
    route = Route.query.order_by(Route.id.desc()).first()
    return render_template("map.html", route_data = route)



'''@socketio.on('newMessage')
def handle_message(userInput):
    prompt = """
        Give locations of great places to visit based off given character traits and interests.
        This person likes: """+traits+"""
    """
    response = model.generate_content(prompt+"| USER UNPUT:"+userInput)
    print(response)

    data = response.text
    socketio.emit('create_message',data)
'''


