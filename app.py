#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from flask import Flask, render_template, redirect, send_from_directory, request
from flask_wtf import FlaskForm, CSRFProtect
from telegram import Update
from wtforms import StringField, TextField
from wtforms.validators import DataRequired

from bot import create_dispatcher, register_handlers
from highlighter import make_image, get_languages
from logic import get_random_bg
from uploader import gen_name_uniq, UPLOAD_DIR

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET")
TG_TOKEN = os.environ.get("TG_TOKEN")
csrf = CSRFProtect(app)

bot, queue, dp = create_dispatcher(TG_TOKEN)
register_handlers(dp)


class MyForm(FlaskForm):
    language = StringField('language')
    code = TextField("code", validators=[DataRequired()])


@app.route('/')
def hello_world():
    return render_template("input.html", languages=get_languages())


@app.route('/upload/<path:filename>')
def image(filename):
    return send_from_directory("upload", filename, as_attachment=('download' in request.args))


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
    path = os.path.join(UPLOAD_DIR, filename + ".jpg")
    if os.path.exists(path):
        return render_template("image.html", image=filename)
    else:
        return render_template("not_found.html"), 404


@app.route('/hook/' + TG_TOKEN, methods=['POST'])
def tg_webhook():
    data = request.get_json(force=True)
    print(data)
    update = Update.de_json(data, bot=bot)
    queue.put(update)
    return "OK"


@app.route('/hook/' + TG_TOKEN, methods=['GET'])
def webhook_get():
    return redirect("https://telegram.me/links_forward_bot", code=302)


if __name__ == '__main__':
    app.run()
