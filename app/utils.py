

class Seq2Vec(object):
    pass


class MetadataGenerator(object):
    def __init__(self, classifier_name, classifier_description, ngrams, author_names, author_email):
        self.classifier_name = classifier_name
        self.classifier_description = classifier_description
        self.ngrams = ngrams
        self.author_names = author_names
        self.author_email = author_email
        self.final = {}

    def generate(self):
        pass

    def __repr__():
        return self.final
