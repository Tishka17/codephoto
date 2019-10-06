import glob
from random import choice


def get_random_bg():
    return choice(glob.glob("templates/pycharm/*.jpg"))
