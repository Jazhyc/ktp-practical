"""Contains auxiliary functions for the main script."""

import json

def load_json(filename):
    """Load the JSON file into a dictionary."""
    with open(filename) as json_file:
        data = json.load(json_file)
    return data