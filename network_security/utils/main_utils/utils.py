import os
import sys
import yaml
import numpy as np
import pickle

from network_security.exceptions.exception import NetworkSecurityException
from network_security.logging.logger import logging


def read_yaml_file(file_path: str) -> dict:
    try:
        # Changed "rb" to "r" with explicit utf-8 encoding for reliable cross-platform reading
        with open(file_path, "r", encoding="utf-8") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise NetworkSecurityException(e, sys)


def write_yaml_file(
    file_path: str,
    content: object,
    replace: bool = False
) -> None:
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Added explicit utf-8 encoding to guarantee clean yaml dumps
        with open(file_path, "w", encoding="utf-8") as file:
            yaml.dump(content, file, default_flow_style=False)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
