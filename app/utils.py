from flask import jsonify
import json
from Bio import SeqIO
from io import StringIO
import os
import git

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


class Seq2Vec(object):
    def __init__(self, sequences, id):
        self.model_id = id
        self.fasta2string(sequences)

    def fasta2string(self, sequences):
        fasta_io = StringIO(sequences)
        sequences = SeqIO.parse(fasta_io, "fasta")
        for seq in sequences:
            print(seq.id)
        fasta_io.close()


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
