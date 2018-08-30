import os
from flask import Flask
from flask_bower import Bower
from config import Config
from flask import render_template, request, make_response, abort
import forms
import utils


repo = utils.RepoController(Config.REPO_URL, Config.REPO_DIR)
classifiers_dict = repo.get_structure()

app = Flask(__name__)
app.config.from_object(Config)
Bower(app)

@app.route("/docs")
def docs():
    return render_template("docs.html")

@app.route("/classifiers")
def classifiers():

    return render_template("classifiers/index.html", classifiers=
                           classifiers_dict)

@app.route("/classifiers/<id>", methods=["GET", "POST"])
def classifier(id):
    try:
        classifier_info = classifiers_dict[id]
    except KeyError:
        return abort(404)
    form = forms.SequenceSubmission()
    if form.validate_on_submit():
        vec = utils.Seq2Vec(form.sequences.data, id,
                            classifier_info["ngrams"],
                            classifier_info["Max Length"])
        
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
