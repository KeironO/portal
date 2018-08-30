from flask import jsonify
import json
from Bio import SeqIO
from io import StringIO
import os
import git
from nltk import ngrams as apply_ngram
from config import Config
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

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
    def __init__(self, sequences, id, ngrams, max_len):
        self.model_id = id
        self.max_len = max_len
        self.ngrams = ngrams
        self.identifiers, self.sequences = self.fasta2string(sequences)

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
            identifiers.append(seq.id)
            seqs.append(str(seq.seq))
            if indx >= 1000:
                break
        fasta_io.close()

        return identifiers, seqs


class ClassifierPredictor(object):
    def __init__(self, id):
        self.model_id = id
        self.get_model()

    def get_model(self):
        model_fp =os.path.join(Config.REPO_DIR, self.model_id, "model.h5")
        self.model = load_model(model_fp)

    def predict(self, s2v):
        predictions = []
        for i in s2v.sequences:
            print(self.model.predict(i))

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
