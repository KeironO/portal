from flask import jsonify
import json
from Bio import SeqIO
from io import StringIO
import os
import git
import numpy as np
from nltk import ngrams as apply_ngram
from config import Config
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras import backend as K

class RepoController(object):
    def __init__(self, repo_url, repo_dir):
        self.repo_url = repo_url
        self.repo_dir = repo_dir

        if os.path.isdir(self.repo_dir) is False:
            self.clone_repo()
        else:
            self.pull_repo()

    def clone_repo(self):
        git.Repo.clone_from(self.repo_url, self.repo_dir)

    def pull_repo(self):
        repo = git.cmd.Git(self.repo_dir)
        repo.pull()

    def get_structure(self):
        dirs = [x for x in os.listdir(self.repo_dir) if os.path.isdir(os.path.join(self.repo_dir, x)) and x != ".git"]
        classifiers_dict = {}
        for model in dirs:
            dir_path = os.path.join(self.repo_dir, model)
            with open(os.path.join(dir_path, "metadata.json"), "rb") as infile:
                classifiers_dict[model] = json.load(infile)
        return classifiers_dict

class Seq2Vec(object):
    def __init__(self, payload, id, ngrams, max_len, limit=1000):
        self.model_id = id
        self.max_len = max_len
        self.ngrams = ngrams

        self.identifiers = list(payload.keys())[0:limit]
        self.sequences = list(payload.values())[0:limit]

        self.sequences = self.ngram()
        self.sequences = self.vectorise()


    def ngram(self):
        sequences = []

        for seq in self.sequences:
            sequences.append(["".join(x) for x in apply_ngram(seq, self.ngrams)])

        return sequences

    def vectorise(self):
        with open(os.path.join(Config.REPO_DIR, self.model_id + "/encoded_values.json"), "rb") as infile:
            encoding_dict = json.load(infile)
        sequences = []
        for seq in self.sequences:
            sequences.append(pad_sequences([[encoding_dict[x] for x in seq]], maxlen=self.max_len))
        return sequences


    def fasta2string(self, sequences):
        fasta_io = StringIO(sequences)
        reads = SeqIO.parse(fasta_io, "fasta")

        identifiers = []
        seqs = []

        for indx, seq in enumerate(reads):
            identifiers.append(seq.name)
            seqs.append(str(seq.seq))
            if indx >= 1000:
                break
        fasta_io.close()

        return identifiers, seqs


class ClassifierPredictor(object):
    def __init__(self, id):
        self.model_id = id
        self.probabilities = []
        self.get_model()

    def get_model(self):
        model_fp =os.path.join(Config.REPO_DIR, self.model_id, "model.h5")
        self.model = load_model(model_fp)


    def decode_predictions(self):

        def _decode(i):
            value_predictions = []
            for indx, prob in enumerate(i):#
                try:
                    value_predictions.append([label_dict[str(indx)][prob.argmax(axis=-1)[0]], float(np.max(prob))])
                except IndexError:
                    #print(prob.argmax(axis=-1), indx, len(i))
                    pass
            return value_predictions


        labels_fp = os.path.join(Config.REPO_DIR, self.model_id, "encoded_labels.json")

        with open(labels_fp, "rb") as infile:
            label_dict = json.load(infile)

        for key, values in label_dict.items():
            temp = dict((v,k) for k,v in values.items())
            label_dict[key] = temp

        predictions_with_scores = []

        for prediction in self.probabilities:
            predictions_with_scores.append(_decode(prediction))

        self.predictions_with_scores = predictions_with_scores


    def predict(self, s2v):
        if len(s2v.sequences) > 0 :
            for seq in s2v.sequences:
                self.probabilities.append(self.model.predict(seq))
        else:
            self.probabilities = self.model.predict(s2v.sequences)
        K.clear_session()

class MetadataGenerator(object):
    def __init__(self, form):
        self.uid = form.uid.data
        self.name = form.name.data
        self.description = form.description.data
        self.ngrams = form.ngrams.data
        self.max_length = form.max_length.data
        self.sequencing_system = form.sequencing_system.data
        self.author_name = form.author_name.data
        self.paired = bool(form.paired.data)
        self.author_email = form.email.data

        self.final = {}

        self.generate()

    def generate(self):
        self.final = {
            "Name": self.name,
            "Description": self.description,
            "ngrams": int(self.ngrams),
            "Max Length": int(self.max_length),
            "Paired": self.paired,
            "Sequencing System": self.sequencing_system,
            "Author Name": self.author_name,
            "Author Email": self.author_email
        }

    def get_json(self):
        return jsonify(self.final)
