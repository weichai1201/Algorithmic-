import json
import os
import pandas as pd


def read_file(file_path):
    if get_file_type(file_path).lower() == 'csv':
        return read_csv(file_path)
    elif get_file_type(file_path).lower() == 'json':
        return read_json(file_path)
    else:
        raise ValueError("Unsupported file format")


def read_csv(file_path):
    return pd.read_csv(file_path)


def read_json(file_path):
    with open(file_path, 'r') as f:
        content = json.load(f)
    return json.dumps(content)


def get_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension[1:]
