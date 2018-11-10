#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from jinja2 import Environment, PackageLoader, select_autoescape
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

env = Environment(
    loader=PackageLoader(__name__, 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template("code.html")


def make_html(content):
    formatter = HtmlFormatter(linenos=True, nobackground=False, style="monokai")
    html = highlight(content, PythonLexer(), formatter)
    css = formatter.get_style_defs('.highlight')
    return template.render(code=html, style=css)


def get_width(content):
    lines = content.split("\n")
    max_width = 0
    for line in lines:
        width = len(line)
        if width > max_width:
            max_width = width
    return max_width


def get_height(content):
    lines = content.split("\n")
    max_height = len(lines)
    return max_height


def make_png(in_html, out_png):
    os.system('xvfb-run -a -s "-screen 0 640x480x16" wkhtmltoimage "%s" "%s"' % (in_html, out_png))
