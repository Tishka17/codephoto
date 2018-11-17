#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import string

import boto3

ALPHABET = string.ascii_letters + string.digits

UPLOAD_DIR = "upload"

os.makedirs(UPLOAD_DIR, exist_ok=True)

s3 = boto3.resource('s3')
bucket = s3.Bucket('codephoto')


def _gen_name(length=5):
    return "".join(random.choice(ALPHABET) for _ in range(length))


def gen_name_uniq(length=5):
    for i in range(length, length * 2):
        for x in range(length):
            name = _gen_name(i)
            if not os.path.exists(os.path.join(UPLOAD_DIR, name + ".jpg")):
                return name


def upload(path, filename, nickname):
    bucket.upload_file(path, "uploads/%s.jpg" % filename, ExtraArgs={'ACL': 'public-read', 'Expires': 7})


def get_info(filename):
    pass
