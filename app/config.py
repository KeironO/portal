import tempfile
import random

class Config(object):
    SECRET_KEY = str(random.getrandbits(64))

    REPO_URL = "https://github.com/KeironO/deepseq2vec-repo"
    REPO_DIR = "deepseq2vec-repo"
    #MAX_CONTENT_LENGTH = 15 * 1024 * 1024

    #STORAGE_DIR = tempfile.gettempdir()
    STORAGE_DIR = "store"