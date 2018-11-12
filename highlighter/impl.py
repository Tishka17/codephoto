#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PIL import Image, ImageChops
from pygments import highlight
from pygments.formatters import ImageFormatter
from pygments.lexers import guess_lexer


def get_formatter(dark):
    if dark:
        return ImageFormatter(
            style="monokai",
            format="png",
            line_numbers=True,
            font_name='DejaVu Sans Mono',
            font_size=14,
            line_number_bg="#272822",
            line_number_fg="#888888",
            image_pad=8,
        )
    return ImageFormatter(
        style="tango",
        format="png",
        line_numbers=True,
        font_name='DejaVu Sans Mono',
        font_size=14,
        line_number_bg="#e0e0e0",
        line_number_fg="#999999",
        image_pad=8,
    )


def limit_input(content: str, max_lines=47) -> str:
    lines = content.splitlines()
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    else:
        lines = lines + [" "] * (max_lines - len(lines))
    return "\n".join(lines)


matrix = [1.33415104e+00, 3.20998746e-02, -4.56420092e+01, 8.66755517e-02,
          1.12526155e+00, -1.99521038e+02, 2.41003654e-04, 3.87679645e-05]


def transofrm(img_file):
    # Import background image
    background_img_raw = Image.open('templates/background.jpg').convert("RGBA")

    foreground_img_raw = Image.open(img_file).convert("RGBA")
    foreground_img_raw = foreground_img_raw.transform(background_img_raw.size, method=Image.PERSPECTIVE, data=matrix,
                                                      fillcolor=(255, 255, 255))

    ImageChops.multiply(foreground_img_raw, background_img_raw, ).save(img_file)


def make_image(content, output, dark=False):
    lexer = guess_lexer(content)
    highlight(limit_input(content), lexer, get_formatter(dark), output)
    transofrm(output)
