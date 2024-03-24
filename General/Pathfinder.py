import os

def get_file_path(filename, folder = None):
    # works only in case file is one level up
    # Get the current working directory (i.e., the directory where this script is located)
    current_path = os.getcwd()
    # Get the parent directory
    path = os.path.dirname(current_path)
    if folder:
        path = os.path.join(path, folder)
    path = os.path.join(path, filename)
    return path



