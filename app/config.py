import tempfile
import random

class Config(object):
    SECRET_KEY = str(random.getrandbits(64))

    REPO_URL = "https://github.com/KeironO/deepseq2vec-repo"
    REPO_DIR = "deepseq2vec-repo"
    #MAX_CONTENT_LENGTH = 15 * 2048 * 2048

    STORAGE_DIR = "store"