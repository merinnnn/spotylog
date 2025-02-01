import sys
import os

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
# import os
from spotylog.excel_utils import save_to_excel, save_to_csv, save_to_json

# Test save_to_excel functionality
def test_save_to_excel():
    data = [
        {"Name": "Believer", "Artists": "Imagine Dragons", "Album": "Evolve"},
        {"Name": "Thunder", "Artists": "Imagine Dragons", "Album": "Evolve"}
    ]
    filename = "test_excel.xlsx"
    save_to_excel(data, filename)

    # Assert the file was created
    assert os.path.exists(filename)
    os.remove(filename)  # Clean up

# Test save_to_csv functionality
def test_save_to_csv():
    data = [
        {"Name": "Believer", "Artists": "Imagine Dragons", "Album": "Evolve"},
        {"Name": "Thunder", "Artists": "Imagine Dragons", "Album": "Evolve"}
    ]
    filename = "test_csv.csv"
    save_to_csv(data, filename)

    # Assert the file was created
    assert os.path.exists(filename)
    os.remove(filename)  # Clean up

# Test save_to_json functionality
def test_save_to_json():
    data = [
        {"Name": "Believer", "Artists": "Imagine Dragons", "Album": "Evolve"},
        {"Name": "Thunder", "Artists": "Imagine Dragons", "Album": "Evolve"}
    ]
    filename = "test_json.json"
    save_to_json(data, filename)

    # Assert the file was created
    assert os.path.exists(filename)
    os.remove(filename)  # Clean up