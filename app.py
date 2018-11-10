#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
import sys

from highlighter import make_html, make_png

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # app.run()
    with open(sys.argv[1]) as f:
        x = make_html(f.read())
    print(x)
    with open("temp.html", "w") as f:
        f.write(x)
    make_png("temp.html", "1.png")