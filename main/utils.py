import os

def check_folder_exist_create(root):
    path = os.makedirs(root, exist_ok=True)
    return path
