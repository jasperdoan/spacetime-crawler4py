import json
import os
import threading
import time


# Global lock object
json_lock = threading.Lock()


def check_data_directory_exists():
    """
    Ensure that the data directory exists.
    """
    data_dir = './data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)



def load_or_initialize_json(file_path, data_format, retries=5, delay=2):
    """
    Load or initialize a JSON file with the specified data format.
    Retries loading the JSON file in case of JSONDecodeError.
    """
    check_data_directory_exists()
    attempt = 0

    while attempt < retries:
        try:
            with json_lock:  # Acquire the lock before reading
                with open(file_path, 'r') as json_file:
                    return json.load(json_file)
        
        # Malformed JSON
        except json.decoder.JSONDecodeError:
            print(f"\tError: The file {file_path} contains malformed JSON. Attempting to recover existing data.\n")
            # Attempt to recover existing data, 5 retries with 2-second delay
            try:
                with json_lock:  # Acquire the lock before reading
                    with open(file_path, 'r') as json_file:
                        existing_data = json_file.read()
                        if existing_data:
                            return json.loads(existing_data)
                        else:
                            return data_format
            except Exception as e:
                print(f"\tError: Failed to recover existing data from {file_path}: {e}\n")
                if attempt < retries:
                    print(f"\tRetrying in {delay} seconds...\n")
                    time.sleep(delay)
                    attempt += 1
                else:
                    # DO NOT LET THIS HAPPEN, progress gone if this happens
                    print("\tMax retries reached. Returning default data format.\n")
                    return data_format

        # Other exceptions
        except FileNotFoundError:
            print(f"\tError: The file {file_path} was not found. Initializing with default data format.\n")
            return data_format

        except PermissionError:
            print(f"\tError: Permission denied when trying to read the file {file_path}.\n")
            raise

        except IOError as e:
            print(f"\tError: An I/O error occurred while reading the file {file_path}: {e}\n")
            raise



def write_json(file_path, data):
    """
    Write data to a JSON file.
    """
    check_data_directory_exists()
    try:
        with json_lock: # Acquire the lock before writing
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file)

    except PermissionError:
        print(f"\tError: Permission denied when trying to write to the file {file_path}.\n")
        raise

    except IOError as e:
        print(f"\tError: An I/O error occurred while writing to the file {file_path}: {e}\n")
        raise