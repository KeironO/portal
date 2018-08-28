import os
from flask import Flask
from flask_bower import Bower
from config import Config
from flask import render_template, request, make_response
import forms
import utils
import json # TODO: Move to utils

dirs = [x for x in os.listdir(Config.REPOSITORY_FP) if os.path.isdir(os.path.join(Config.REPOSITORY_FP, x)) and x != ".git"]

classifiers_dict = {

}

for model in dirs:
    dir_path = os.path.join(Config.REPOSITORY_FP, model)

    with open(os.path.join(dir_path, "metadata.json"), "rb") as infile:
        classifiers_dict[model] = json.load(infile)


app = Flask(__name__)
app.config.from_object(Config)
Bower(app)

@app.route("/docs")
def docs():
    return "Help page goes here."


@app.route("/classifiers")
def classifiers():
    return render_template("classifiers/index.html", classifiers_dict=classifiers_dict)

@app.route("/classifiers/<id>", methods=["GET", "POST"])
def classifier(id):
    classifier_info = classifiers_dict[id]
    form = forms.SequenceSubmission()
    if form.validate_on_submit():
        utils.Seq2Vec(form.sequences.data)
    return render_template("classifiers/classifier.html", id=id,
                           info=classifier_info, form=form)

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
