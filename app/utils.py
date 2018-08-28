from flask import jsonify
import json
from Bio import SeqIO
from io import StringIO

class Seq2Vec(object):
    def __init__(self, sequences, id):
        self.model_id = id
        self.fasta2string(sequences)

    def fasta2string(self, sequences):
        fasta_io = StringIO(sequences)
        records = SeqIO.parse(fasta_io, "fasta")
        for i in records:
            print(i.id)
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
