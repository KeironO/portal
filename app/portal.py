import os
from flask import Flask
from flask_bower import Bower
from collections import OrderedDict
from config import Config
import json
from flask import render_template, request, make_response, abort, redirect, url_for, session, jsonify
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

    download_url = Config.REPO_URL + "/blob/master/"+ id + "/training_file.fasta?raw=true"

    if form.validate_on_submit():
        vec = utils.Seq2Vec(form.sequences.data, id,
                            classifier_info["ngrams"],
                            classifier_info["Max Length"])
        clf = utils.ClassifierPredictor(id)
        clf.predict(vec)
        clf.decode_predictions()

        out_length = max([len(x) for x in clf.predictions_with_scores])
        results = zip([*vec.identifiers], clf.predictions_with_scores)
        return render_template("classifiers/results.html", results=results, out_length=out_length)
    return render_template("classifiers/classifier.html", id=id,
                           info=classifier_info, form=form,
                           download_url=download_url)


@app.route("/classifiers/<model_id>/api/", methods=["POST"])
def classifier_api(model_id):
    try:
        classifier_info = classifiers_dict[model_id]
    except KeyError:
        return abort(404)

    if request.method == "POST":
        payload = request.get_json()
        vec = utils.Seq2Vec(payload, model_id, classifier_info["ngrams"], classifier_info["Max Length"])
        clf = utils.ClassifierPredictor(model_id)
        clf.predict(vec)
        clf.decode_predictions()

        results = {}
        for index, seq_id in enumerate(vec.identifiers):
            results[seq_id] = OrderedDict(clf.predictions_with_scores[index])

        response = app.response_class(
            response=json.dumps(results),
            status=200,
            mimetype='application/json'
        )
        return response



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
