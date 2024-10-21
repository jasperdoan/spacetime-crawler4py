import json
import os
import threading


# Global lock object
json_write_lock = threading.Lock()


def check_data_directory_exists():
    """
    Ensure that the data directory exists.
    """
    data_dir = './data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)



def load_or_initialize_json(file_path, data_format):
    """
    Load or initialize a JSON file with the specified data format.
    """
    check_data_directory_exists()
    try:
        with open(file_path, 'r') as json_file:
            return json.load(json_file)
    except json.decoder.JSONDecodeError:
        print(f"Error: The file {file_path} contains malformed JSON. Initializing with default data format.")
        return data_format
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found. Initializing with default data format.")
        return data_format
    except PermissionError:
        print(f"Error: Permission denied when trying to read the file {file_path}.")
        raise
    except IOError as e:
        print(f"Error: An I/O error occurred while reading the file {file_path}: {e}")
        raise



def write_json(file_path, data):
    """
    Write data to a JSON file.
    """
    check_data_directory_exists()
    try:
        with json_write_lock:  # Use the lock to synchronize access
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file)
    except PermissionError:
        print(f"Error: Permission denied when trying to write to the file {file_path}.")
        raise
    except IOError as e:
        print(f"Error: An I/O error occurred while writing to the file {file_path}: {e}")
        raise