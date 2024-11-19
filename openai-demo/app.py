from flask import Flask, render_template, request
from bot import ask_question
from markupsafe import Markup


app = Flask(__name__)

new_question="Is god real?"

default_style = "background-color: white"

@app.route('/')
def index():
	answer = ask_question(new_question)
	return render_template("index.html", bot_response=answer, color='white',body_style=default_style, form_style=default_style,response_style=default_style ,h1_style=default_style)

@app.route('/', methods = ['POST'])
def index_post():
	new_question = request.form['question']
	rap, body_style, h1_style, form_style,response_style = ask_question(new_question)

	
	return render_template("index.html", bot_response= Markup(rap), color='white',body_style=Markup(body_style), form_style=Markup(form_style),response_style=Markup(response_style) ,h1_style=Markup(h1_style))