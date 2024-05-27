import os
import json
from datetime import datetime
from loguru import logger


def save_json(data: dict, filename: str) -> None:
    """
    Saves the provided data to a specified JSON file.

    Parameters:
    data (dict): The data to be saved.
    filename (str): The file name where the data will be saved.
    """
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        logger.info(f"Data saved to JSON file {filename}.")
    except Exception as e:
        logger.error(f"Failed to save JSON data: {e}")


def load_json(filename: str) -> dict:
    """
    Loads data from a specified JSON file.

    Parameters:
    filename (str): The file name from which to load the data.

    Returns:
    dict: Loaded data from the JSON file.
    """
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            logger.info(f"Data loaded from JSON file {filename}.")
            return data
        except Exception as e:
            logger.error(f"Failed to load JSON data: {e}")
            return {}
    else:
        logger.warning(f"JSON file {filename} does not exist.")
        return {}


def save_generation_error(data: str):
    """
    Saves the provided error data to a log file.

    Parameters:
    data (str): The error data to be saved.
    """

    data = f"Error occurred at {datetime.now()}:\n{data}\n"
    log_dir = "data"
    log_file = "generation_error.log"
    log_path = os.path.join(log_dir, log_file)

    try:
        # Ensure the directory exists
        os.makedirs(log_dir, exist_ok=True)

        # Open the file in append mode and write the data
        with open(log_path, "a") as file:
            file.write(data)
        logger.info("Error data saved to generation_error.log.")

    except Exception as e:
        logger.error(f"Failed to save error data: {e}")
