#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import guess_lexer

template = env.get_template("code.html")

light_formatter = ImageFormatter(
    style="tango",
    format="png",
    line_numbers=True,
    font_name='DejaVu Sans Mono',
    font_size=14,
    line_number_bg="#e0e0e0",
    line_number_fg="#999999",
    image_pad=8,
)

dark_formatter = ImageFormatter(
    style="monokai",
    format="png",
    line_numbers=True,
    font_name='DejaVu Sans Mono',
    font_size=14,
    line_number_bg="#272822",
    line_number_fg="#888888",
    image_pad=8,
)


def limit_input(content: str, max_lines=48) -> str:
    return "\n".join(content.splitlines()[:max_lines])


def make_image(content, output, dark=False):
    lexer = guess_lexer(content)
    highlight(limit_input(content), lexer, dark_formatter if dark else light_formatter, output)
