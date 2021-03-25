import os


def get_data_folder():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
