from flask import jsonify

class Seq2Vec(object):
    pass


class MetadataGenerator(object):
    def __init__(self, form):
        self.name = form.name
        self.description = form.description
        self.ngrams = form.ngrams
        self.max_length = form.ngrams
        self.author_name = form.author_name
        self.author_email = form.email

        self.final = {}

        self.generate()

    def generate(self):
        self.final = {
            "name": self.name.data,
            "description": self.description.data,
            "ngrams": self.ngrams.data,
            "max len": self.max_length.data,
            "author name": self.author_name.data,
            "author email": self.author_email.data,
        }

    def get_json(self):
        return jsonify(results=self.final)
