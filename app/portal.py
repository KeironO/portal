import os
from flask import Flask
from flask_bower import Bower
from flask import render_template

import utils

app = Flask(__name__)
Bower(app)

@app.route("/docs")
def docs():
    return "Help page goes here."

@app.route("/classifiers")
def classifiers():
    return render_template("classifier.html")

@app.route("/")
def index():
    return render_template("index.html")
