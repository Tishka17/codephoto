#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from flask import Flask, render_template, request, redirect, send_from_directory

from highlighter import make_image
from uploader import gen_name_uniq, UPLOAD_DIR

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("input.html")


@app.route("/code", methods=["POST"])
def render_code():
    code = request.form["code"]
    name = gen_name_uniq(5)
    make_image(code, os.path.join(UPLOAD_DIR, name))
    return redirect("/i/" + name)


@app.route('/i/<path:filename>')
def custom_static(filename):
    return send_from_directory(UPLOAD_DIR, filename)


if __name__ == '__main__':
    app.run()
    # with open(sys.argv[1]) as f:
    #     data = f.read()
    # x = make_image(data, "1.png", False)
    # x = make_image(data, "2.png", True)
