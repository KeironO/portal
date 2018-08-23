import os
from flask import Flask
from flask_bower import Bower
from flask import render_template


app = Flask(__name__)
Bower(app)


@app.route("/help")
def help():
    return "Help page goes here."

@app.route("/classifier")
def classifier():
    return None

@app.route("/")
def main():
    return render_template("index.html")
