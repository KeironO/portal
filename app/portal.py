#!/usr/bin/env python

import os
from flask import Flask
from flask_bower import Bower
from collections import OrderedDict
from config import Config
import json
from flask import render_template, request, make_response, abort, redirect, url_for, session, jsonify
from flask.views import MethodView
import uuid
import forms
import utils
import requests
import datetime
import tempfile

repo = utils.RepoController(Config.REPO_URL, Config.REPO_DIR)
classifiers_dict = repo.get_structure()

app = Flask(__name__)
app.config.from_object(Config)
Bower(app)

if os.path.isdir(Config.STORAGE_DIR) is False:
    os.mkdir(Config.STORAGE_DIR)

@app.route("/docs")
def docs():
    return render_template("docs.html")

@app.route("/classifiers")
def classifiers():
    blank = {"#" : None}
    identifiers = list(classifiers_dict.keys())
    splits = [[{y: classifiers_dict[y]} for y in identifiers[x:x+2]] for x in range(0, len(identifiers), 2)]

    for index, i in enumerate(splits):
        if len(i) < 2:
            for i in range(2 - len(i)):
                splits[index].append(blank)

    return render_template("classifiers/index.html", splits=splits)

@app.route("/classifiers/<model_id>", methods=["GET", "POST"])
def classifier(model_id):
    try:
        classifier_info = classifiers_dict[model_id]
    except KeyError:
        return abort(404)
    form = forms.SequenceSubmission()

    download_url = Config.REPO_URL + "/blob/master/"+ model_id + "/training_file.fasta?raw=true"

    if form.validate_on_submit():

        if type(form.sequences_file.data) != str:
            sequence_data = str(form.sequences_file.data.read().decode("utf-8"))
            payload = utils.Fasta2Dict(sequence_data).payload
        else:
            payload = utils.Fasta2Dict(form.sequences.data).payload
        job_hash = uuid.uuid4().hex
        job_fp = os.path.join(Config.STORAGE_DIR, job_hash + ".json")


        job_details = {
            "job_hash": job_hash,
            "time": datetime.datetime.now().isoformat(),
            "ip": request.remote_addr,
            "model_id" : model_id,
            "payload": payload
        }

        with open(job_fp, "w") as outfile:
            json.dump(job_details, outfile)

        session["job_fp"] = job_fp

        return redirect(url_for("results", model_id=model_id, job_hash=job_hash))

    return render_template("classifiers/classifier.html", model_id=model_id,
                           info=classifier_info, form=form,
                           download_url=download_url)


@app.route("/classifiers/<model_id>/results/<job_hash>", methods=["GET"])
def results(model_id, job_hash):
    return render_template("classifiers/results.html")

@app.route("/classifiers/<model_id>/results/<job_hash>/get/", methods=["GET"])
def results_getter(model_id, job_hash):
    with open(session["job_fp"], "r") as infile:
        job_details = json.load(infile)
    
    if "results" in job_details:
        return jsonify(job_details["results"])
    else:
        api_url = "".join(request.url_root[:-1]) + url_for("api", model_id=job_details["model_id"])
        response = requests.post(api_url, json=job_details["payload"])
        if response.status_code == 200:
            parser = {"_items" : []}
            for key, values in response.json().items():
                parser["_items"].append({"seq_id":key, "predictions" : values})

            job_details["results"] = parser
            with open(session["job_fp"], "w") as outfile:
                json.dump(job_details, outfile, indent=4)
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
