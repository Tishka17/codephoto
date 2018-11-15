#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from typing import List, Dict

from PIL import Image, ImageChops
from pygments import highlight
from pygments.lexers import guess_lexer

from .formatter import Formatter


def get_formatter(dark):
    if dark:
        return Formatter(
            style="monokai",
            format="png",
            line_numbers=True,
            font_name='DejaVu Sans Mono',
            font_size=14,
            line_number_bg="#272822",
            line_number_fg="#888888",
            image_pad=8,
        )
    return Formatter(
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


matrix_cache: Dict[str, List[int]] = {}


def get_matrix_file(background: str) -> str:
    return background.rsplit(".", maxsplit=1)[0] + ".json"


def get_matrix(bg):
    if bg not in matrix_cache:
        with open(get_matrix_file(bg)) as f:
            matrix_cache[bg] = json.load(f)["coefficients"]
    return matrix_cache[bg]


def transform(img, img_file, background, matrix=None):
    background_img_raw = Image.open(background).convert("RGBA")
    if matrix is None:
        matrix = get_matrix(background)

    foreground_img_raw = img
    foreground_img_raw = foreground_img_raw.transform(background_img_raw.size, method=Image.PERSPECTIVE, data=matrix,
                                                      resample=Image.BILINEAR, fillcolor=(255, 255, 255))

    ImageChops.multiply(foreground_img_raw, background_img_raw).save(img_file)


def make_image(content, output, background, dark=False, matrix=None):
    lexer = guess_lexer(content)
    formatter = get_formatter(dark)
    highlight(limit_input(content), lexer, formatter, output)
    transform(formatter.image, output, background, matrix)
