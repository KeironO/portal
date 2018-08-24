import os
from flask import Flask
from flask_bower import Bower
from config import Config
from flask import render_template, request

import forms

import utils

app = Flask(__name__)
app.config.from_object(Config)
Bower(app)


@app.route("/docs")
def docs():
    return "Help page goes here."


@app.route("/classifiers")
def classifiers():
    return render_template("classifier.html")


@app.route("/contribute", methods=["GET", "POST"])
def contribute():
    form = forms.MetadataGeneratorForm(request.form)
    if form.validate_on_submit():
        print(form)

    return render_template("contribute.html", form=form)


@app.route("/")
def index():
    return render_template("index.html")
