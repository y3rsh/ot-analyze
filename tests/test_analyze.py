import json
from pathlib import Path

from ot_analyze import analyze, generate_analysis_path

import test_data.data as td


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
    check_no_errors_in_analysis(generate_analysis_path(td.POSITIVE_OT2))


def test_analyze_flex_positive():
    analyze(td.POSITIVE_FLEX)
    check_no_errors_in_analysis(generate_analysis_path(td.POSITIVE_FLEX))


def test_analyze_ot2_negative():
    analyze(td.ERROR)
    check_errors_in_analysis(generate_analysis_path(td.ERROR))


def test_analyze_flex_negative():
    analyze(td.FLEX_ERROR)
    check_errors_in_analysis(generate_analysis_path(td.FLEX_ERROR))


def test_analyze_json_positive():
    analyze(td.JSON_POSITIVE)
    check_no_errors_in_analysis(generate_analysis_path(td.JSON_POSITIVE))


def test_analyze_json_error():
    analyze(td.JSON_ERROR)
    check_errors_in_analysis(generate_analysis_path(td.JSON_ERROR))
