import os


def build_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)