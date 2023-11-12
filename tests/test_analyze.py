import json
from pathlib import Path

import pytest
from ot_analyze import (
    analyze,
)

import test_data.data as td


def delete_analysis_files():
    analysis_files = list(Path("test_data").rglob("**/*analysis.json"))
    for analysis in analysis_files:
        if analysis.exists():
            try:
                analysis.unlink()  # Deletes the file
                print(f"Deleted {analysis.resolve()}")
            except Exception as e:
                print(f"Error deleting {analysis.resolve()}: {e}")


@pytest.fixture(scope="session", autouse=True)
def clear_analysis_files():
    delete_analysis_files()


def check_no_errors_in_analysis(analysis: Path):
    if not analysis.exists():
        raise FileNotFoundError(f"The file {analysis} does not exist")

    with open(analysis, "r") as file:
        data = json.load(file)
        assert "errors" in data, "The 'errors' key is not in the JSON data"
        assert data["errors"] == [], f"Expected errors to be [], but found {data['errors']}"


def check_errors_in_analysis(analysis: Path):
    if not analysis.exists():
        raise FileNotFoundError(f"The file {analysis} does not exist")

    with open(analysis, "r") as file:
        data = json.load(file)
        assert "errors" in data, "The 'errors' key is not in the JSON data"
        assert data["errors"] != [], "Expected errors, but found nothing"


def test_analyze_ot2_positive():
    analyze(td.POSITIVE_OT2)
    check_no_errors_in_analysis(Path(td.POSITIVE_OT2.parent, "analysis.json"))


def test_analyze_flex_positive():
    analyze(td.POSITIVE_FLEX)
    check_no_errors_in_analysis(Path(td.POSITIVE_FLEX.parent, "analysis.json"))


def test_analyze_ot2_negative():
    analyze(td.ERROR)
    check_errors_in_analysis(Path(td.ERROR.parent, "analysis.json"))
