import json


def load_or_initialize_json(file_path, data_format):
    """
    Load or initialize a JSON file with the specified data format.
    """
    try:
        with open(file_path, 'r') as json_file:
            return json.load(json_file)

    # Exception handling for malformed JSON data or incorrect format + First time creating the file
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return data_format



def write_json(file_path, data):
    """
    Write data to a JSON file.
    """
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)