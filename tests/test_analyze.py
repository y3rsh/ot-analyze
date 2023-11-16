import json
from pathlib import Path

from ot_analyze import analyze, generate_analysis_path, ProtocolPaths

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
    protocol_path = ProtocolPaths(td.POSITIVE_OT2, generate_analysis_path(td.POSITIVE_OT2))
    analyze(protocol_path)
    check_no_errors_in_analysis(protocol_path.analysis_file)


def test_analyze_flex_positive():
    protocol_path = ProtocolPaths(td.POSITIVE_FLEX, generate_analysis_path(td.POSITIVE_FLEX))
    analyze(protocol_path)
    check_no_errors_in_analysis(protocol_path.analysis_file)


def test_analyze_ot2_negative():
    protocol_path = ProtocolPaths(td.ERROR, generate_analysis_path(td.ERROR))
    analyze(protocol_path)
    check_errors_in_analysis(protocol_path.analysis_file)


def test_analyze_flex_negative():
    protocol_path = ProtocolPaths(td.FLEX_ERROR, generate_analysis_path(td.FLEX_ERROR))
    analyze(protocol_path)
    check_errors_in_analysis(protocol_path.analysis_file)


def test_analyze_json_positive():
    protocol_path = ProtocolPaths(td.JSON_POSITIVE, generate_analysis_path(td.JSON_POSITIVE))
    analyze(protocol_path)
    check_no_errors_in_analysis(protocol_path.analysis_file)


def test_analyze_json_error():
    protocol_path = ProtocolPaths(td.JSON_ERROR, generate_analysis_path(td.JSON_ERROR))
    analyze(protocol_path)
    check_errors_in_analysis(protocol_path.analysis_file)
