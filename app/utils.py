from flask import jsonify

class Seq2Vec(object):
    pass


class MetadataGenerator(object):
    def __init__(self, form):
        self.uid = form.uid.data
        self.name = form.name.data
        self.description = form.description.data
        self.ngrams = form.ngrams.data
        self.max_length = form.max_length.data
        self.author_name = form.author_name.data
        self.author_email = form.email.data

        self.final = {}

        self.generate()

    def generate(self):
        self.final = {
            "name": self.name,
            "description": self.description,
            "ngrams": int(self.ngrams),
            "max len": int(self.max_length),
            "author name": self.author_name,
            "author email": self.author_email,
        }

    def get_json(self):
        return jsonify(results=self.final)
