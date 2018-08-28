import os
from flask import Flask
from flask_bower import Bower
from config import Config
from flask import render_template, request, make_response

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
        metadata = utils.MetadataGenerator(form)
        response = make_response(metadata.get_json())
        response.headers["Content-Disposition"] = "attachment; filename=metadata.json"
        return response
    return render_template("contribute.html", form=form)


@app.route("/")
def index():
    return render_template("index.html")
