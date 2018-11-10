#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
import sys

from highlighter import make_image

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # app.run()
    with open(sys.argv[1]) as f:
        data = f.read()
    x = make_image(data, "1.png", False)
    x = make_image(data, "2.png", True)