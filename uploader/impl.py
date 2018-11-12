#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import string

ALPHABET = string.ascii_letters + string.digits

UPLOAD_DIR = "upload"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def _gen_name(len=5):
    return "".join(random.choice(ALPHABET) for _ in range(len))


def gen_name_uniq(len=5):
    for i in range(len, len * 2):
        for x in range(len):
            name = _gen_name(i) + ".png"
            if not os.path.exists(os.path.join(UPLOAD_DIR, name)):
                return name
