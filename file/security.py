from os.path import *
import os


def is_backward_access(file_location):
    return ".." in file_location


def is_readable(file_location):
    return os.access(file_location, os.R_OK)


def is_accessible(dir_location):
    return os.access(dir_location, os.R_OK) and os.access(dir_location, os.X_OK)