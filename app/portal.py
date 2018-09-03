import os
from flask import Flask
from flask_bower import Bower
from collections import OrderedDict
from config import Config
import json
from flask import render_template, request, make_response, abort, redirect, url_for, session, jsonify
from flask.views import MethodView
import forms
import utils
import requests

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

@app.route("/classifiers/<model_id>", methods=["GET", "POST"])
def classifier(model_id):
    try:
        classifier_info = classifiers_dict[model_id]
    except KeyError:
        return abort(404)
    form = forms.SequenceSubmission()

    download_url = Config.REPO_URL + "/blob/master/"+ model_id + "/training_file.fasta?raw=true"

    if form.validate_on_submit():
        payload = utils.Fasta2Dict(form.sequences.data).payload
        session["payload"] = payload
        session["api_url"] = request.url + "/api/"
        return redirect(url_for("results", model_id=model_id))

    return render_template("classifiers/classifier.html", model_id=model_id,
                           info=classifier_info, form=form,
                           download_url=download_url)


@app.route("/classifiers/<model_id>/results", methods=["GET"])
def results(model_id):
    return render_template("classifiers/results.html")

@app.route("/classifiers/<model_id>/results/get", methods=["GET"])
def results_getter(model_id):
    response = requests.post(session["api_url"], json=session["payload"])
    if response.status_code == 200:
        parser = {"_items" : []}
        for key, values in response.json().items():
            parser["_items"].append({"seq_id":key, "predictions" : values})
        return jsonify(parser)
    else:
        abort(500)

@app.route("/classifiers/<model_id>/api/", methods=["POST"])
def api(model_id):
    if request.method == "POST":
        try:
            classifier_info = classifiers_dict[model_id]
        except KeyError:
            return abort(404)
        payload = request.get_json()
        vec = utils.Seq2Vec(payload, model_id, classifier_info["ngrams"], classifier_info["Max Length"])
        clf = utils.ClassifierPredictor(model_id)
        clf.predict(vec)
        clf.decode_predictions()

        results = {}
        for index, seq_id in enumerate(vec.identifiers):
            results[seq_id] = clf.predictions_with_scores[index]

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
