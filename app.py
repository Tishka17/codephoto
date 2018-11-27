#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import glob
import os
import random
import string

from flask import Flask, render_template, redirect, send_from_directory
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextField
from wtforms.validators import DataRequired

from highlighter import make_image, get_languages
from uploader import gen_name_uniq, UPLOAD_DIR

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET")
csrf = CSRFProtect(app)


class MyForm(FlaskForm):
    language = StringField('language')
    code = TextField("code", validators=[DataRequired()])


@app.route('/')
def hello_world():
    return render_template("input.html", languages=get_languages())


@app.route('/upload/<path:filename>')
def image(filename):
    return send_from_directory("upload", filename)


def get_random_bg():
    return random.choice(glob.glob("templates/pycharm/*.jpg"))


@app.route("/code", methods=["POST"])
def render_code():
    form = MyForm()
    if not form.validate():
        return redirect("/")
    name = gen_name_uniq(5)
    path = os.path.join(UPLOAD_DIR, name + ".jpg")
    make_image(form.code.data, path, form.language.data, background=get_random_bg())
    # upload(path, name, nickname)
    return redirect("/i/" + name)


@app.route('/i/<path:filename>')
def custom_static(filename):
    return render_template("image.html", image=filename)


if __name__ == '__main__':
    app.run()
