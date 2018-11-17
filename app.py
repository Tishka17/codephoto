#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import random

from flask import Flask, render_template, request, redirect, send_from_directory

from highlighter import make_image, get_languages
from uploader import gen_name_uniq, UPLOAD_DIR

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("input.html", languages=get_languages())


@app.route('/upload/<path:filename>')
def image(filename):
    return send_from_directory("upload", filename)


def get_random_bg():
    return "templates/pycharm/%s.jpg" % random.randint(1, 8)


@app.route("/code", methods=["POST"])
def render_code():
    code = request.form["code"]
    lang = request.form["language"]
    name = gen_name_uniq(5)
    path = os.path.join(UPLOAD_DIR, name + ".jpg")
    make_image(code, path, lang, background=get_random_bg())
    # upload(path, name, nickname)
    return redirect("/i/" + name)


@app.route('/i/<path:filename>')
def custom_static(filename):
    return render_template("image.html", image=filename)


if __name__ == '__main__':
    app.run()
