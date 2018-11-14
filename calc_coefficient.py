#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys

import numpy

from highlighter import make_image, get_matrix_file


def find_coeffs(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0] * t[0], -s[0] * t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1] * t[0], -s[1] * t[1]])
    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(source_coords).reshape(8)
    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return list(numpy.array(res).reshape(8))


orig = [(0, 0), (828, 0), (828, 721), (0, 721)]

# pycharm2
# highlighter.impl.matrix = find_coeffs(
#     [(0, 0), (828, 0), (828, 721), (0, 721)],
#     [(52, 136), (708, 133), (683, 808), (46, 774)])


background: str = sys.argv[1]
translated = [
    tuple(map(int, x.split(":"))) for x in sys.argv[2:]
]

out = get_matrix_file(background)

# pycharm
matrix = find_coeffs(orig, translated)

with open(__file__) as f:
    code = f.read()
make_image(code, "3.png", background=background, matrix=matrix)

with open(out, "w") as f:
    json.dump({
        "corners_original": orig,
        "corners_translated": translated,
        "coefficients": matrix
    }, f, indent=2, ensure_ascii=False)
# translated = [(38, 140), (880, 133), (880, 915), (30, 891)]
