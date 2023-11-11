import json
from pathlib import Path
import pytest
from ot_analyze import (
    analyze,
)  # replace with the actual name of your module containing the analyze function

POSITIVE_OT2 = Path("test_data", "positive_ot2_no_labware")
POSITIVE_FLEX = Path("test_data", "positive_flex")
ERROR = Path("test_data", "error")
NO_CI = Path("test_data", "no_ci")
NO_PROTOCOL = Path("test_data", "no_protocol")

# Creating an array of these paths
test_directories = [POSITIVE_OT2, POSITIVE_FLEX, ERROR, NO_CI, NO_PROTOCOL]


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
    delete_analysis_files(test_directories)


def check_errors_in_json(analysis: Path):
    if not analysis.exists():
        raise FileNotFoundError(f"The file {analysis} does not exist")

    with open(analysis, "r") as file:
        data = json.load(file)
        assert "errors" in data, "The 'errors' key is not in the JSON data"
        assert (
            data["errors"] == []
        ), f"Expected errors to be [], but found {data['errors']}"


def test_analyze_ot2_positive():
    analyze(POSITIVE_OT2)
    check_errors_in_json(Path(POSITIVE_OT2, "analysis.json"))
