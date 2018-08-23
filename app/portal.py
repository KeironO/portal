import os
from flask import Flask

app = Flask(__name__)

@app.route("/help")
def help():
    return "Help page goes here."

@app.route("/classifier")
def classifier():
    return None

@app.route("/")
def main():
    return "Hello World"
