import json
from pathlib import Path

import pytest
from src.ot_analyze import (
    analyze,
)

import test_data.data as td


def delete_analysis_files(directories):
    for directory in directories:
        analysis_file = Path(directory) / "analysis.json"
        if analysis_file.exists():
            try:
                analysis_file.unlink()  # Deletes the file
                print(f"Deleted 'analysis.json' in {directory}")
            except Exception as e:
                print(f"Error deleting 'analysis.json' in {directory}: {e}")


@pytest.fixture(scope="session", autouse=True)
def clear_analysis_files():
    delete_analysis_files(td.ALL)


def check_errors_in_json(analysis: Path):
    if not analysis.exists():
        raise FileNotFoundError(f"The file {analysis} does not exist")

    with open(analysis, "r") as file:
        data = json.load(file)
        assert "errors" in data, "The 'errors' key is not in the JSON data"
        assert data["errors"] == [], f"Expected errors to be [], but found {data['errors']}"


def test_analyze_ot2_positive():
    analyze(td.POSITIVE_OT2)
    check_errors_in_json(Path(td.POSITIVE_OT2, "analysis.json"))


def test_analyze_flex_positive():
    analyze(td.POSITIVE_FLEX)
    check_errors_in_json(Path(td.POSITIVE_FLEX, "analysis.json"))
